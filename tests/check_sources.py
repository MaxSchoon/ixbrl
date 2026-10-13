#!/usr/bin/env python3
"""The source registry the monthly maintenance cycle re-reads.

maintenance/sources.json lists, per topic, the primary sources a cycle
re-reads and the files they keep current. This check holds it to shape:

  1. every topic names a task the routine runs (maintenance/README.md):
     jurisdictions, new-mandates, topics or skill-craft;
  2. every topic names files that exist, and every source has a publisher,
     an https URL, what to watch for, and a `checked_on` date that is a real
     date and not in the future;
  3. every jurisdiction reference under references/jurisdictions/ is watched
     by at least one topic, so a regime added for a new mandate cannot ship
     without the sources that keep it current;
  4. every task has at least one topic, and no URL is listed twice.

With `--max-age DAYS` it also reports every source whose `checked_on` is
older than that: the list a cycle still owes. CI runs it without the flag,
so the age of a source never turns an unrelated pull request red.

Run: python3 tests/check_sources.py [--max-age DAYS] [--today YYYY-MM-DD]
Exit codes: 0 clean, 1 a problem or (with --max-age) a stale source, 2 usage.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "maintenance" / "sources.json"
TASKS = ("jurisdictions", "new-mandates", "topics", "skill-craft")
SOURCE_FIELDS = ("publisher", "url", "watch", "checked_on")


def parse_day(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def problems_in(
    registry: dict, root: Path, today: date, max_age: int | None = None
) -> tuple[list[str], list[str]]:
    """(shape problems, stale sources) for a parsed registry."""
    problems: list[str] = []
    stale: list[str] = []
    topics = registry.get("topics")
    if not isinstance(topics, list) or not topics:
        return ["registry has no topics"], []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    watched: set[str] = set()
    tasks: set[str] = set()
    for position, topic in enumerate(topics):
        if not isinstance(topic, dict):
            problems.append(f"topic #{position + 1} is not an object")
            continue
        tid = topic.get("id", "?")
        if tid in seen_ids:
            problems.append(f"topic {tid}: duplicate id")
        seen_ids.add(tid)
        task = topic.get("task")
        if task not in TASKS:
            problems.append(f"topic {tid}: task must be one of {', '.join(TASKS)}")
        else:
            tasks.add(task)
        files = topic.get("files") or []
        if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
            problems.append(f"topic {tid}: files must be a list of paths")
            files = []
        elif not files:
            problems.append(f"topic {tid}: names no file it keeps current")
        for rel in files:
            if not (root / rel).is_file():
                problems.append(f"topic {tid}: file {rel} does not exist")
            watched.add(rel)
        sources = topic.get("sources") or []
        if not isinstance(sources, list):
            problems.append(f"topic {tid}: sources must be a list")
            sources = []
        elif not sources:
            problems.append(f"topic {tid}: lists no source")
        for source in sources:
            if not isinstance(source, dict):
                problems.append(f"topic {tid}: a source is not an object")
                continue
            missing = [f for f in SOURCE_FIELDS if not source.get(f)]
            if missing:
                problems.append(f"topic {tid}: a source lacks {', '.join(missing)}")
                continue
            url = source["url"]
            if not isinstance(url, str):
                problems.append(f"topic {tid}: a source url is not a string")
                continue
            if not url.startswith("https://"):
                problems.append(f"topic {tid}: {url} is not https")
            if url in seen_urls:
                problems.append(f"topic {tid}: {url} is listed twice")
            seen_urls.add(url)
            day = parse_day(source["checked_on"])
            if day is None:
                problems.append(f"topic {tid}: {url} checked_on is not YYYY-MM-DD")
            elif day > today:
                problems.append(f"topic {tid}: {url} checked_on {day} is in the future")
            elif max_age is not None and (today - day).days > max_age:
                stale.append(f"{tid}: {url} last read {day}")
    for path in sorted((root / "references" / "jurisdictions").glob("*.md")):
        rel = path.relative_to(root).as_posix()
        if rel not in watched:
            problems.append(f"{rel} is watched by no topic in {REGISTRY.name}")
    for task in TASKS:
        if task not in tasks:
            problems.append(f"no topic runs the {task} task")
    return problems, stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--max-age", type=int, metavar="DAYS")
    parser.add_argument("--today", type=parse_day, help="the date to judge age at")
    args = parser.parse_args(argv)
    today = args.today or date.today()
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"::error::{REGISTRY.name}: {error}")
        return 1
    problems, stale = problems_in(registry, ROOT, today, args.max_age)
    for line in problems:
        print(f"::error::{line}")
    for line in stale:
        print(f"stale: {line}")
    count = sum(
        len(t["sources"]) if isinstance(t.get("sources"), list) else 0
        for t in registry.get("topics", [])
        if isinstance(t, dict)
    )
    if not problems and not stale:
        topics = len(registry["topics"])
        print(f"Source registry OK ({count} sources across {topics} topics)")
    return 1 if problems or stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
