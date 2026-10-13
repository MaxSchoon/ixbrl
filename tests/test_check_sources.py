#!/usr/bin/env python3
"""Tests for tests/check_sources.py, the maintenance source registry.

Hermetic: the repository's own registry is read, and every negative case is
an edited copy of it in memory, judged against a fixed date.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_sources as cs

REGISTRY = json.loads(cs.REGISTRY.read_text(encoding="utf-8"))
TODAY = date(2026, 10, 13)


def check(registry: dict, max_age: int | None = None) -> tuple[list[str], list[str]]:
    return cs.problems_in(registry, cs.ROOT, TODAY, max_age)


class Registry(unittest.TestCase):
    def test_committed_registry_is_clean(self):
        self.assertEqual(check(REGISTRY), ([], []))

    def test_every_jurisdiction_file_must_be_watched(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"] = [t for t in reg["topics"] if t["id"] != "hk-ird"]
        problems, _ = check(reg)
        self.assertTrue(any("hk-ird.md is watched by no topic" in p for p in problems))

    def test_a_source_needs_every_field_and_https(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"][0]["sources"].append(
            {
                "publisher": "x",
                "url": "http://example.org",
                "watch": "y",
                "checked_on": "2026-10-01",
            }
        )
        reg["topics"][0]["sources"].append({"publisher": "x", "url": "https://a.b"})
        problems, _ = check(reg)
        self.assertTrue(any("is not https" in p for p in problems))
        self.assertTrue(any("lacks watch, checked_on" in p for p in problems))

    def test_dates_must_be_real_and_not_ahead(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"][0]["sources"][0]["checked_on"] = "2026-13-01"
        reg["topics"][1]["sources"][0]["checked_on"] = "2026-12-01"
        problems, _ = check(reg)
        self.assertTrue(any("not YYYY-MM-DD" in p for p in problems))
        self.assertTrue(any("in the future" in p for p in problems))

    def test_unknown_task_missing_file_and_duplicate_url(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"][0]["task"] = "gardening"
        reg["topics"][0]["files"] = ["references/nope.md"]
        reg["topics"][1]["sources"].append(dict(reg["topics"][2]["sources"][0]))
        problems, _ = check(reg)
        self.assertTrue(any("task must be one of" in p for p in problems))
        self.assertTrue(any("references/nope.md does not exist" in p for p in problems))
        self.assertTrue(any("is listed twice" in p for p in problems))

    def test_malformed_entries_are_reported_not_crashed_on(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"].append("not a topic")
        reg["topics"][0]["sources"].append("not a source")
        reg["topics"][1]["sources"].append(
            {"publisher": "x", "url": 42, "watch": "y", "checked_on": "2026-10-01"}
        )
        problems, _ = check(reg)
        self.assertTrue(any("is not an object" in p for p in problems), problems)
        self.assertTrue(any("url is not a string" in p for p in problems), problems)

    def test_every_task_needs_a_topic(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"] = [t for t in reg["topics"] if t["task"] != "skill-craft"]
        problems, _ = check(reg)
        self.assertIn("no topic runs the skill-craft task", problems)

    def test_max_age_names_what_a_cycle_still_owes(self):
        reg = copy.deepcopy(REGISTRY)
        reg["topics"][0]["sources"][0]["checked_on"] = "2026-08-01"
        problems, stale = check(reg, max_age=40)
        self.assertEqual(problems, [])
        self.assertEqual(len(stale), 1)
        self.assertIn("last read 2026-08-01", stale[0])
        self.assertEqual(check(reg)[1], [])

    def test_cli_is_green_without_max_age(self):
        self.assertEqual(cs.main(["--today", "2026-10-13"]), 0)


if __name__ == "__main__":
    unittest.main()
