#!/usr/bin/env python3
"""Deterministic skill eval: the score a hillclimb on this skill moves.

An edit to SKILL.md or a reference is kept only when it holds every bar here.
The eval is a proxy, and says so: it measures what can be measured without a
model in the loop, so it runs in CI on every pull request and gives the same
number twice.

  trigger      does the frontmatter `description` win a query against the
               descriptions of neighbouring skills (evals/distractors.json)?
               Positive cases must win; negative cases must not.
  route        does the SKILL.md reference index send the query to the file
               that answers it? Reported as mean reciprocal rank and hit@1.
  fact         does the named file still state a fact the skill must carry
               (a current release, a regulation number, a mandate date)?

Each case is in one split. `train` cases are the ones a maintainer reads
while editing. `test` cases are held out: never read while choosing an edit,
never copied into the skill, scored only to accept or refuse one. The result
of a cycle is the test-split delta, not the train-split one.

`evals/baseline.json` freezes the accepted scores, the digest of every
held-out case and the digest of this harness. `--check` (CI) fails when:

  * a metric on either split falls below its frozen value (less the metric's
    declared tolerance);
  * a held-out case was edited or removed, or added without a freeze;
  * this file or the distractor set changed since the freeze (the harness
    changed, so its old numbers no longer compare);
  * a safety floor breaks: SKILL.md over 32 KiB or 500 lines, a description
    over 1024 characters, a held-out query copied into the skill, or a
    release row dropped from any *DTS and vintages* table (historical
    applicability and acceptance windows are kept, never pruned).

`--freeze --reason "..."` records a new baseline. It refuses to lower any
metric and refuses to edit or remove a held-out case, so the bar only
ratchets up. A release row may leave a vintages table only by naming it with
`--drop-row` in that freeze, which records the reason.

Run: python3 tests/eval_skill.py [--check | --freeze --reason TEXT] [--json]
Exit codes: 0 clean, 1 a bar failed, 2 usage error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
EVALS = ROOT / "evals"
CASES = EVALS / "cases.json"
DISTRACTORS = EVALS / "distractors.json"
BASELINE = EVALS / "baseline.json"
HARNESS = (Path(__file__).resolve(), DISTRACTORS)

SPLITS = ("train", "test")
KINDS = ("trigger", "negative", "route", "fact")
# Declared slack per metric. Every metric is deterministic, so this is not a
# noise allowance: it absorbs the small rank shifts that adding a reference
# row causes through IDF. A freeze still refuses any decrease, so the slack
# cannot accumulate across cycles.
TOLERANCE = {
    "trigger_recall": 0.0,
    "trigger_specificity": 0.0,
    "route_mrr": 0.02,
    "route_hit1": 0.0,
    "fact_recall": 0.0,
}
MAX_SKILL_BYTES = 32 * 1024
MAX_BODY_LINES = 500
MAX_DESCRIPTION_CHARS = 1024
# A held-out query counts as leaked when this many consecutive words of it
# appear in the skill text.
LEAK_WORDS = 8

STOPWORD_TEXT = (
    "a an and are as at be by can do does for from has have how i if in into "
    "is it its me my no not of on or our should so that the their them then "
    "there these this to was we what when where which who why will with would "
    "you your about any all one two get use used using need want"
)
STOPWORDS = frozenset(STOPWORD_TEXT.split())
TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    """Lower-case word tokens, stopwords out, a crude plural fold.

    `EFM.6.05.20` becomes `efm 6 05 20` and `xbrldie:PrimaryItem` becomes
    `xbrldie primaryitem`, which is what lets a validator code in a query meet
    the same code in an index row.
    """
    out = []
    for tok in TOKEN.findall(text.lower()):
        if tok in STOPWORDS:
            continue
        if len(tok) > 4 and tok.endswith("s") and not tok.endswith("ss"):
            tok = tok[:-1]
        out.append(tok)
    return out


class BM25:
    """Okapi BM25 over a small fixed corpus (k1 1.2, b 0.75)."""

    def __init__(self, docs: list[str]) -> None:
        self.docs = [Counter(tokens(d)) for d in docs]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.docs), 1)
        df: Counter[str] = Counter()
        for d in self.docs:
            df.update(d.keys())
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: str) -> list[float]:
        terms = set(tokens(query))
        out = []
        for doc, length in zip(self.docs, self.lengths, strict=True):
            s = 0.0
            for t in terms:
                f = doc.get(t, 0)
                if f:
                    norm = f + 1.2 * (1 - 0.75 + 0.75 * length / self.avg)
                    s += self.idf[t] * f * 2.2 / norm
            out.append(s)
        return out


def rank_of(scores: list[float], index: int) -> int:
    """1-based rank of `index`; ties count against it (no lucky ordering)."""
    return 1 + sum(1 for i, s in enumerate(scores) if i != index and s >= scores[index])


# --- reading the skill --------------------------------------------------------


def frontmatter_description(text: str) -> str:
    match = re.search(r"(?m)^description:\s*(.+)$", text.split("\n---", 1)[0])
    return match.group(1).strip() if match else ""


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


ROW_TARGET = re.compile(r"`((?:references|assets)/[^`]*)`|<(https://[^>]+)>")


def index_rows(text: str) -> list[tuple[str, str]]:
    """(row text, target path) for each row of the SKILL.md reference index."""
    rows = []
    for line in section(text, "Reference index").splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        target = ROW_TARGET.search(cells[-1])
        if target:
            path = target.group(1).rstrip("/") if target.group(1) else target.group(2)
            rows.append((" ".join(cells[:-1]), path))
    return rows


VINTAGE_HEADER = re.compile(r"^\|\s*Release\s*\|")


def vintage_rows() -> dict[str, list[str]]:
    """Release keys of every *DTS and vintages* table, per file.

    The key is the first cell with emphasis and code marks removed, cut at the
    first parenthesis or semicolon, so marking a row current (bold) or adding
    a note after the release name does not count as removing it.
    """
    out: dict[str, list[str]] = {}
    for path in sorted((ROOT / "references").rglob("*.md")):
        keys: list[str] = []
        in_table = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if VINTAGE_HEADER.match(line):
                in_table = True
                continue
            if not in_table:
                continue
            if not line.startswith("|"):
                in_table = False
                continue
            if line.startswith("|---"):
                continue
            first = line.strip().strip("|").split("|")[0]
            first = re.sub(r"[*`]", "", first)
            first = re.split(r"[(;]", first)[0]
            key = " ".join(first.split()).lower()
            if key:
                keys.append(key)
        if keys:
            out[path.relative_to(ROOT).as_posix()] = keys
    return out


# --- scoring ------------------------------------------------------------------


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def case_digest(case: dict) -> str:
    blob = json.dumps(case, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def harness_digest() -> str:
    h = hashlib.sha256()
    for path in HARNESS:
        h.update(path.name.encode())
        h.update(path.read_bytes())
    return h.hexdigest()[:16]


def validate_cases(cases: list[dict]) -> list[str]:
    problems = []
    seen: set[str] = set()
    for case in cases:
        cid = case.get("id", "?")
        if cid in seen:
            problems.append(f"case {cid}: duplicate id")
        seen.add(cid)
        if case.get("split") not in SPLITS:
            problems.append(f"case {cid}: split must be one of {SPLITS}")
        if case.get("kind") not in KINDS:
            problems.append(f"case {cid}: kind must be one of {KINDS}")
        if case.get("kind") in ("trigger", "negative", "route") and not case.get(
            "query"
        ):
            problems.append(f"case {cid}: needs a query")
        if case.get("kind") == "route" and not case.get("expect"):
            problems.append(f"case {cid}: a route case names the file it expects")
        if case.get("kind") == "fact":
            if not (case.get("file") and case.get("pattern")):
                problems.append(f"case {cid}: a fact case needs file and pattern")
            else:
                try:
                    re.compile(case["pattern"])
                except re.error as error:
                    problems.append(f"case {cid}: bad pattern: {error}")
    return problems


def score(cases: list[dict], skill_text: str, distractors: list[dict]) -> dict:
    """Per-split metrics and per-case outcomes for the given skill text."""
    description = frontmatter_description(skill_text)
    skills = BM25([description] + [d["description"] for d in distractors])
    rows = index_rows(skill_text)
    router = BM25([r[0] for r in rows])
    targets = [r[1] for r in rows]

    outcomes: dict[str, dict] = {}
    for case in cases:
        kind, cid = case["kind"], case["id"]
        if kind in ("trigger", "negative"):
            s = skills.scores(case["query"])
            wins = rank_of(s, 0) == 1 and s[0] > 0
            outcomes[cid] = {"pass": wins if kind == "trigger" else not wins}
        elif kind == "route":
            s = router.scores(case["query"])
            ranks = [
                rank_of(s, i) for i, t in enumerate(targets) if t == case["expect"]
            ]
            best = min(ranks) if ranks else None
            outcomes[cid] = {
                "pass": best == 1,
                "rank": best,
                "rr": 1 / best if best else 0.0,
            }
        else:
            path = ROOT / case["file"]
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            found = re.search(case["pattern"], text, re.S) is not None
            outcomes[cid] = {"pass": found}

    metrics: dict[str, dict[str, float]] = {}
    for split in SPLITS:
        mine = [c for c in cases if c["split"] == split]

        def frac(kind: str, mine: list[dict] = mine) -> float:
            group = [outcomes[c["id"]]["pass"] for c in mine if c["kind"] == kind]
            return round(sum(group) / len(group), 4) if group else 1.0

        routes = [outcomes[c["id"]]["rr"] for c in mine if c["kind"] == "route"]
        metrics[split] = {
            "trigger_recall": frac("trigger"),
            "trigger_specificity": frac("negative"),
            "route_mrr": round(sum(routes) / len(routes), 4) if routes else 1.0,
            "route_hit1": frac("route"),
            "fact_recall": frac("fact"),
        }
    return {"metrics": metrics, "outcomes": outcomes}


def floors(skill_text: str, cases: list[dict]) -> list[str]:
    """Absolute bars that hold whatever the baseline says."""
    problems = []
    size = len(skill_text.encode("utf-8"))
    if size > MAX_SKILL_BYTES:
        problems.append(f"SKILL.md is {size} bytes, over {MAX_SKILL_BYTES}")
    lines = skill_text.count("\n") + 1
    if lines > MAX_BODY_LINES:
        problems.append(f"SKILL.md is {lines} lines, over {MAX_BODY_LINES}")
    desc = frontmatter_description(skill_text)
    if len(desc) > MAX_DESCRIPTION_CHARS:
        problems.append(f"description is {len(desc)} chars, over 1024")
    corpus = " ".join(
        TOKEN.findall(
            " ".join(
                [skill_text]
                + [
                    p.read_text(encoding="utf-8")
                    for p in sorted((ROOT / "references").rglob("*.md"))
                ]
            ).lower()
        )
    )
    for case in cases:
        if case["split"] != "test" or not case.get("query"):
            continue
        words = TOKEN.findall(case["query"].lower())
        for i in range(len(words) - LEAK_WORDS + 1):
            shingle = " ".join(words[i : i + LEAK_WORDS])
            if f" {shingle} " in f" {corpus} ":
                problems.append(
                    f"held-out case {case['id']} leaked into the skill: '{shingle}'"
                )
                break
    return problems


def compare(
    current: dict, baseline: dict, cases: list[dict], rows: dict[str, list[str]]
) -> list[str]:
    """What `--check` refuses, relative to the frozen baseline."""
    problems = []
    if baseline.get("harness") != harness_digest():
        problems.append(
            "the harness (tests/eval_skill.py or evals/distractors.json) changed "
            "since the freeze; review the change, then re-freeze"
        )
    frozen = baseline.get("heldout", {})
    test_now = {c["id"]: case_digest(c) for c in cases if c["split"] == "test"}
    for cid, digest in sorted(frozen.items()):
        if cid not in test_now:
            problems.append(f"held-out case {cid} was removed")
        elif test_now[cid] != digest:
            problems.append(f"held-out case {cid} was edited")
    for cid in sorted(set(test_now) - set(frozen)):
        problems.append(f"held-out case {cid} is not frozen yet; run --freeze")
    for split in SPLITS:
        for metric, value in current["metrics"][split].items():
            bar = baseline["metrics"][split].get(metric)
            if bar is None:
                continue
            if value < bar - TOLERANCE.get(metric, 0.0):
                problems.append(f"{split} {metric} fell to {value} (frozen {bar})")
    for path, keys in sorted(baseline.get("vintages", {}).items()):
        now = set(rows.get(path, []))
        for key in keys:
            if key not in now:
                problems.append(f"{path}: release row '{key}' was removed")
    return problems


def freeze(
    current: dict,
    baseline: dict | None,
    cases: list[dict],
    rows: dict[str, list[str]],
    reason: str,
    drop: list[str],
) -> tuple[dict | None, list[str]]:
    """A new baseline, or the reasons it is refused."""
    problems = []
    vintages = {p: list(k) for p, k in rows.items()}
    if baseline:
        for split in SPLITS:
            for metric, value in current["metrics"][split].items():
                bar = baseline["metrics"][split].get(metric)
                if bar is not None and value < bar:
                    problems.append(
                        f"refusing to lower {split} {metric} from {bar} to {value}"
                    )
        test_now = {c["id"]: case_digest(c) for c in cases if c["split"] == "test"}
        for cid, digest in baseline.get("heldout", {}).items():
            if test_now.get(cid) != digest:
                problems.append(f"refusing: held-out case {cid} edited or removed")
        for path, keys in baseline.get("vintages", {}).items():
            for key in keys:
                if key in rows.get(path, []):
                    continue
                if f"{path}:{key}" in drop:
                    continue
                problems.append(
                    f"refusing: {path} release row '{key}' is gone; name it with "
                    f"--drop-row '{path}:{key}' if removing it is intended"
                )
    if problems:
        return None, problems
    history = list((baseline or {}).get("history", []))
    history.append({"on": date.today().isoformat(), "reason": reason, "dropped": drop})
    return {
        "frozen_on": date.today().isoformat(),
        "harness": harness_digest(),
        "metrics": current["metrics"],
        "tolerance": TOLERANCE,
        "heldout": {c["id"]: case_digest(c) for c in cases if c["split"] == "test"},
        "vintages": vintages,
        "history": history,
    }, []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="hold the frozen bars")
    mode.add_argument("--freeze", action="store_true", help="record a new baseline")
    parser.add_argument("--reason", help="why this freeze (required with --freeze)")
    parser.add_argument(
        "--drop-row",
        action="append",
        default=[],
        metavar="FILE:KEY",
        help="a vintages row this freeze removes on purpose",
    )
    parser.add_argument("--json", action="store_true", help="print the full report")
    args = parser.parse_args(argv)
    if args.freeze and not args.reason:
        parser.error("--freeze needs --reason")

    cases = load_json(CASES)["cases"]
    bad = validate_cases(cases)
    if bad:
        for line in bad:
            print(f"::error::{line}")
        return 2
    skill_text = SKILL.read_text(encoding="utf-8")
    current = score(cases, skill_text, load_json(DISTRACTORS)["skills"])
    rows = vintage_rows()
    baseline = load_json(BASELINE) if BASELINE.is_file() else None

    problems = floors(skill_text, cases)
    if args.freeze:
        new, refused = freeze(
            current, baseline, cases, rows, args.reason, args.drop_row
        )
        problems += refused
        if new is not None and not problems:
            BASELINE.write_text(
                json.dumps(new, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
            )
    elif baseline is None:
        problems.append("no frozen baseline: run --freeze --reason 'first baseline'")
    else:
        problems += compare(current, baseline, cases, rows)

    if args.json:
        print(json.dumps({**current, "problems": problems}, indent=1))
    else:
        for split in SPLITS:
            line = ", ".join(f"{k} {v}" for k, v in current["metrics"][split].items())
            print(f"{split}: {line}")
        failed = sorted(c for c, o in current["outcomes"].items() if not o["pass"])
        print(f"cases not passing: {', '.join(failed) if failed else 'none'}")
        for line in problems:
            print(f"::error::{line}")
        if not problems:
            print("Skill eval OK" + (" (baseline frozen)" if args.freeze else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
