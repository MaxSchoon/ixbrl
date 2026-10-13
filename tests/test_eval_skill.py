#!/usr/bin/env python3
"""Tests for tests/eval_skill.py, the hillclimb bars of this skill.

Hermetic: the scorer reads the repository's own SKILL.md, references and
evals/ files, and every negative case below works on an edited copy of that
text in memory. Nothing is written to the repository; a freeze is exercised
through the `freeze()` function, never through the CLI.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import io
import json
import re
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import eval_skill as ev

SKILL_TEXT = ev.SKILL.read_text(encoding="utf-8")
CASES = ev.load_json(ev.CASES)["cases"]
DISTRACTORS = ev.load_json(ev.DISTRACTORS)["skills"]


def without_row(text: str, target: str) -> str:
    """SKILL.md with the reference-index row for `target` deleted."""
    return "\n".join(
        line
        for line in text.splitlines()
        if not (line.startswith("|") and f"`{target}`" in line.split("|")[-2])
    )


class Tokens(unittest.TestCase):
    def test_validator_codes_split_into_matchable_parts(self):
        self.assertEqual(ev.tokens("EFM.6.05.20"), ["efm", "6", "05", "20"])
        self.assertIn("xbrldie", ev.tokens("xbrldie:PrimaryItemError"))

    def test_plural_fold_and_stopwords(self):
        self.assertEqual(ev.tokens("the dimensions"), ["dimension"])
        self.assertEqual(ev.tokens("class"), ["class"])

    def test_a_tie_counts_against_the_expected_row(self):
        self.assertEqual(ev.rank_of([1.0, 1.0, 0.0], 0), 2)
        self.assertEqual(ev.rank_of([0.0, 0.0], 1), 2)
        self.assertEqual(ev.rank_of([2.0, 1.0], 0), 1)


class ReadingTheSkill(unittest.TestCase):
    def test_every_reference_index_row_has_a_target(self):
        rows = ev.index_rows(SKILL_TEXT)
        targets = {t for _, t in rows}
        self.assertIn("references/dimensions.md", targets)
        self.assertIn("references/jurisdictions/nl-sbr.md", targets)
        self.assertIn("assets", targets)
        self.assertIn("https://filings.xbrl.org/", targets)
        table = ev.section(SKILL_TEXT, "Reference index")
        body_rows = [
            ln for ln in table.splitlines() if re.match(r"^\| (?!---|Read when)", ln)
        ]
        self.assertEqual(len(rows), len(body_rows))

    def test_every_route_case_expects_an_indexed_file(self):
        targets = {t for _, t in ev.index_rows(SKILL_TEXT)}
        for case in CASES:
            if case["kind"] == "route":
                self.assertIn(case["expect"], targets, case["id"])

    def test_vintage_keys_ignore_emphasis_and_notes(self):
        rows = ev.vintage_rows()
        self.assertIn("references/esef.md", rows)
        for keys in rows.values():
            for key in keys:
                self.assertEqual(key, key.lower())
                self.assertNotRegex(key, r"[*`(;]")
        esef = rows["references/esef.md"]
        self.assertIn("esef 2024", esef)
        self.assertIn("2025", esef)


class Scoring(unittest.TestCase):
    def test_cases_are_valid_and_both_splits_cover_every_kind(self):
        self.assertEqual(ev.validate_cases(CASES), [])
        for split in ev.SPLITS:
            kinds = {c["kind"] for c in CASES if c["split"] == split}
            self.assertEqual(kinds, set(ev.KINDS), split)

    def test_invalid_cases_are_named(self):
        bad = [
            {"id": "a", "split": "dev", "kind": "route", "query": "q"},
            {"id": "a", "split": "train", "kind": "fact", "file": "x", "pattern": "("},
        ]
        problems = ev.validate_cases(bad)
        self.assertTrue(any("duplicate id" in p for p in problems))
        self.assertTrue(any("split must be" in p for p in problems))
        self.assertTrue(any("expects" in p for p in problems))
        self.assertTrue(any("bad pattern" in p for p in problems))

    def test_same_input_same_score(self):
        one = ev.score(CASES, SKILL_TEXT, DISTRACTORS)
        two = ev.score(CASES, SKILL_TEXT, DISTRACTORS)
        self.assertEqual(one, two)

    def test_removing_an_index_row_fails_its_route_cases(self):
        """The refuter: a degraded skill must score lower, and --check must say so."""
        degraded = without_row(SKILL_TEXT, "references/dimensions.md")
        self.assertNotEqual(degraded, SKILL_TEXT)
        before = ev.score(CASES, SKILL_TEXT, DISTRACTORS)
        after = ev.score(CASES, degraded, DISTRACTORS)
        for case in CASES:
            if case.get("expect") == "references/dimensions.md":
                self.assertFalse(after["outcomes"][case["id"]]["pass"], case["id"])
        baseline = ev.load_json(ev.BASELINE)
        problems = ev.compare(after, baseline, CASES, ev.vintage_rows())
        self.assertTrue(any("route" in p and "fell" in p for p in problems), problems)
        self.assertLess(
            after["metrics"]["test"]["route_mrr"], before["metrics"]["test"]["route_mrr"]
        )

    def test_a_description_without_its_trigger_words_stops_triggering(self):
        gutted = re.sub(
            r"(?m)^description:.*$",
            "description: Use for documents.",
            SKILL_TEXT,
            count=1,
        )
        after = ev.score(CASES, gutted, DISTRACTORS)
        self.assertLess(after["metrics"]["train"]["trigger_recall"], 0.5)

    def test_a_fact_removed_from_its_file_fails(self):
        case = {
            "id": "f",
            "split": "train",
            "kind": "fact",
            "file": "references/esef.md",
            "pattern": r"no such release 1999",
        }
        out = ev.score([case], SKILL_TEXT, DISTRACTORS)
        self.assertFalse(out["outcomes"]["f"]["pass"])
        self.assertEqual(out["metrics"]["train"]["fact_recall"], 0.0)


class Floors(unittest.TestCase):
    def test_repository_holds_every_floor(self):
        self.assertEqual(ev.floors(SKILL_TEXT, CASES), [])

    def test_oversize_skill_breaks_the_floor(self):
        problems = ev.floors(SKILL_TEXT + "x" * ev.MAX_SKILL_BYTES, CASES)
        self.assertTrue(any("bytes" in p for p in problems))

    def test_a_held_out_query_copied_into_the_skill_is_a_leak(self):
        held = next(c for c in CASES if c["split"] == "test" and c["kind"] == "route")
        leaked = SKILL_TEXT + "\n" + held["query"] + "\n"
        problems = ev.floors(leaked, CASES)
        self.assertTrue(any(held["id"] in p and "leaked" in p for p in problems))

    def test_a_train_query_in_the_skill_is_not_a_leak(self):
        train = next(c for c in CASES if c["split"] == "train" and c["kind"] == "route")
        self.assertEqual(ev.floors(SKILL_TEXT + train["query"], CASES), [])


class Baseline(unittest.TestCase):
    def setUp(self):
        self.current = ev.score(CASES, SKILL_TEXT, DISTRACTORS)
        self.rows = ev.vintage_rows()
        self.baseline = ev.load_json(ev.BASELINE)

    def test_committed_baseline_holds(self):
        self.assertEqual(ev.compare(self.current, self.baseline, CASES, self.rows), [])

    def test_baseline_freezes_every_held_out_case_and_the_harness(self):
        held = {c["id"] for c in CASES if c["split"] == "test"}
        self.assertEqual(set(self.baseline["heldout"]), held)
        self.assertEqual(self.baseline["harness"], ev.harness_digest())

    def test_an_edited_held_out_case_is_refused(self):
        cases = json.loads(json.dumps(CASES))
        held = next(c for c in cases if c["split"] == "test")
        held["query"] = held.get("query", "") + " (reworded)"
        problems = ev.compare(self.current, self.baseline, cases, self.rows)
        self.assertTrue(any(f"{held['id']} was edited" in p for p in problems))
        _, refused = ev.freeze(self.current, self.baseline, cases, self.rows, "r", [])
        self.assertTrue(any("edited or removed" in p for p in refused))

    def test_a_removed_held_out_case_is_refused(self):
        held = next(c for c in CASES if c["split"] == "test")
        cases = [c for c in CASES if c is not held]
        problems = ev.compare(self.current, self.baseline, cases, self.rows)
        self.assertTrue(any(f"{held['id']} was removed" in p for p in problems))

    def test_a_new_held_out_case_must_be_frozen(self):
        cases = [
            *CASES,
            {"id": "zz-new", "split": "test", "kind": "negative", "query": "bake"},
        ]
        problems = ev.compare(self.current, self.baseline, cases, self.rows)
        self.assertTrue(any("zz-new is not frozen" in p for p in problems))

    def test_freeze_never_lowers_a_metric(self):
        lower = json.loads(json.dumps(self.current))
        lower["metrics"]["test"]["route_mrr"] -= 0.01
        new, refused = ev.freeze(lower, self.baseline, CASES, self.rows, "r", [])
        self.assertIsNone(new)
        self.assertTrue(any("refusing to lower test route_mrr" in p for p in refused))

    def test_check_tolerates_only_the_declared_slack(self):
        within = json.loads(json.dumps(self.current))
        within["metrics"]["test"]["route_mrr"] = (
            self.baseline["metrics"]["test"]["route_mrr"] - 0.01
        )
        self.assertEqual(ev.compare(within, self.baseline, CASES, self.rows), [])
        beyond = json.loads(json.dumps(self.current))
        beyond["metrics"]["test"]["fact_recall"] = (
            self.baseline["metrics"]["test"]["fact_recall"] - 0.01
        )
        problems = ev.compare(beyond, self.baseline, CASES, self.rows)
        self.assertTrue(any("fact_recall fell" in p for p in problems))

    def test_freeze_ratchets_up_and_keeps_history(self):
        higher = json.loads(json.dumps(self.current))
        higher["metrics"]["train"]["route_hit1"] = 1.0
        new, refused = ev.freeze(higher, self.baseline, CASES, self.rows, "why", [])
        self.assertEqual(refused, [])
        assert new is not None
        self.assertEqual(new["metrics"]["train"]["route_hit1"], 1.0)
        self.assertEqual(new["history"][-1]["reason"], "why")
        self.assertEqual(len(new["history"]), len(self.baseline["history"]) + 1)

    def test_a_dropped_release_row_is_refused_unless_named(self):
        path, keys = next(iter(self.baseline["vintages"].items()))
        rows = {**self.rows, path: [k for k in self.rows[path] if k != keys[0]]}
        problems = ev.compare(self.current, self.baseline, CASES, rows)
        self.assertTrue(any(f"'{keys[0]}' was removed" in p for p in problems))
        new, refused = ev.freeze(self.current, self.baseline, CASES, rows, "r", [])
        self.assertIsNone(new)
        self.assertTrue(any("--drop-row" in p for p in refused))
        new, refused = ev.freeze(
            self.current, self.baseline, CASES, rows, "r", [f"{path}:{keys[0]}"]
        )
        self.assertEqual(refused, [])
        assert new is not None
        self.assertEqual(new["history"][-1]["dropped"], [f"{path}:{keys[0]}"])

    def test_a_changed_harness_is_refused(self):
        stale = {**self.baseline, "harness": "0" * 16}
        problems = ev.compare(self.current, stale, CASES, self.rows)
        self.assertTrue(any("harness" in p for p in problems))


class Cli(unittest.TestCase):
    def test_check_is_green_and_prints_the_same_thing_twice(self):
        outputs = []
        for _ in range(2):
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = ev.main(["--check"])
            self.assertEqual(code, 0, buf.getvalue())
            outputs.append(buf.getvalue())
        self.assertEqual(outputs[0], outputs[1])

    def test_freeze_without_a_reason_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as raised, redirect_stdout(io.StringIO()):
            ev.main(["--freeze"])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
