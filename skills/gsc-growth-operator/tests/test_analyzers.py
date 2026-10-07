#!/usr/bin/env python3
"""Regression tests for the local GSC export and sitemap utilities."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
SKILL_DIR = TEST_DIR.parent
FIXTURES = TEST_DIR / "fixtures"
ANALYZER = SKILL_DIR / "scripts" / "gsc_analyze.py"
SITEMAP = SKILL_DIR / "scripts" / "sitemap_audit.py"


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script), *args], text=True, capture_output=True, check=False)


def payload(process: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(process.stdout)


class GscAnalyzerTests(unittest.TestCase):
    def common(self) -> list[str]:
        return ["--property", "sc-domain:example.com", "--as-of-date", "2026-10-02", "--country", "US"]

    def test_overview_applies_freshness_filters_and_explicit_url_normalization(self) -> None:
        process = run(ANALYZER, "overview", "--input", str(FIXTURES / "performance.csv"), *self.common(), "--normalize-urls", "safe")
        self.assertEqual(process.returncode, 0, process.stderr)
        result = payload(process)
        self.assertEqual(result["input"]["rows_excluded_by_freshness"], 1)
        self.assertEqual(result["input"]["rows_excluded_by_dimension_filter"], 1)
        self.assertEqual(result["input"]["rows_after_filters"], 4)
        self.assertEqual(result["export_totals"]["clicks"], 28.0)
        self.assertIsNone(result["property_totals"])
        self.assertEqual(result["top_pages"][0]["page"], "https://example.com/widgets")
        self.assertEqual(result["top_pages"][0]["clicks"], 25.0)

    def test_invalid_date_and_negative_metrics_fail_clearly(self) -> None:
        invalid_date = run(ANALYZER, "overview", "--input", str(FIXTURES / "invalid-date.csv"), "--freshness-days", "0")
        negative = run(ANALYZER, "overview", "--input", str(FIXTURES / "negative.csv"), "--freshness-days", "0")
        nonfinite = run(ANALYZER, "overview", "--input", str(FIXTURES / "nonfinite.csv"), "--freshness-days", "0")
        empty = run(ANALYZER, "overview", "--input", str(FIXTURES / "empty.csv"), "--freshness-days", "0")
        self.assertEqual(invalid_date.returncode, 2)
        self.assertIn("invalid ISO date", invalid_date.stderr)
        self.assertEqual(negative.returncode, 2)
        self.assertIn("at least 0", negative.stderr)
        self.assertEqual(nonfinite.returncode, 2)
        self.assertIn("non-finite", nonfinite.stderr)
        self.assertEqual(empty.returncode, 2)
        self.assertIn("empty export", empty.stderr)

    def test_strict_mode_rejects_duplicate_dimension_rows(self) -> None:
        process = run(ANALYZER, "overview", "--input", str(FIXTURES / "duplicate.csv"), "--property", "sc-domain:example.com", "--as-of-date", "2026-10-02", "--strict")
        self.assertEqual(process.returncode, 2)
        self.assertIn("duplicate dimension", process.stderr)

    def test_compare_separates_gainers_and_losers_and_drops_filters_non_declines(self) -> None:
        args = ["--current", str(FIXTURES / "current.csv"), "--baseline", str(FIXTURES / "baseline.csv"), "--property", "sc-domain:example.com", "--as-of-date", "2026-10-02", "--freshness-days", "0"]
        comparison = run(ANALYZER, "compare", *args)
        drops = run(ANALYZER, "drops", *args, "--min-click-loss", "5", "--min-relative-click-loss", "0.2")
        self.assertEqual(comparison.returncode, 0, comparison.stderr)
        self.assertEqual(drops.returncode, 0, drops.stderr)
        compare_result, drops_result = payload(comparison), payload(drops)
        self.assertEqual(compare_result["gainers"][0]["query"], "acme widgets")
        self.assertEqual(compare_result["losers"][0]["query"], "buy widgets")
        self.assertEqual([row["query"] for row in drops_result["candidates"]], ["buy widgets"])

    def test_decay_requires_two_full_lookback_windows(self) -> None:
        process = run(ANALYZER, "decay", "--current", str(FIXTURES / "current.csv"), "--baseline", str(FIXTURES / "baseline.csv"), "--property", "sc-domain:example.com", "--as-of-date", "2026-10-02", "--freshness-days", "0")
        self.assertEqual(process.returncode, 2)
        self.assertIn("requires two 90-day windows", process.stderr)

    def test_compare_rejects_mismatched_aggregation_dimensions(self) -> None:
        process = run(ANALYZER, "compare", "--current", str(FIXTURES / "current.csv"), "--baseline", str(FIXTURES / "baseline-no-country.csv"), "--property", "sc-domain:example.com", "--as-of-date", "2026-10-02", "--freshness-days", "0")
        self.assertEqual(process.returncode, 2)
        self.assertIn("incompatible aggregation dimensions", process.stderr)

    def test_ctr_requires_a_benchmark_for_click_gap_claims(self) -> None:
        no_benchmark = run(ANALYZER, "ctr", "--input", str(FIXTURES / "performance.csv"), *self.common(), "--min-impressions", "10", "--min-cohort-size", "1")
        with_benchmark = run(ANALYZER, "ctr", "--input", str(FIXTURES / "performance.csv"), *self.common(), "--min-impressions", "10", "--min-cohort-size", "1", "--benchmark", str(FIXTURES / "ctr-benchmark.csv"))
        self.assertEqual(no_benchmark.returncode, 0, no_benchmark.stderr)
        self.assertEqual(with_benchmark.returncode, 0, with_benchmark.stderr)
        self.assertEqual(payload(no_benchmark)["analysis"], "ctr_screen")
        benchmarked = payload(with_benchmark)
        self.assertEqual(benchmarked["analysis"], "ctr_opportunities")
        self.assertTrue(all("estimated_click_gap" in item for item in benchmarked["candidates"]))

    def test_missing_position_is_excluded_from_position_normalized_screen(self) -> None:
        process = run(ANALYZER, "ctr", "--input", str(FIXTURES / "performance.csv"), "--property", "sc-domain:example.com", "--as-of-date", "2026-10-05", "--country", "US", "--min-impressions", "10", "--min-cohort-size", "1")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(payload(process)["excluded_missing_position_entity_count"], 1)

    def test_brand_split_keeps_ambiguous_and_excluded_metrics(self) -> None:
        process = run(ANALYZER, "brand", "--input", str(FIXTURES / "performance.csv"), *self.common(), "--brand", "Acme", "--ambiguous", "acme jobs", "--exclude", "acme competitor")
        self.assertEqual(process.returncode, 0, process.stderr)
        segments = payload(process)["segments"]
        self.assertEqual(segments["branded"]["clicks"], 20.0)
        self.assertEqual(segments["ambiguous"]["clicks"], 2.0)
        self.assertEqual(segments["excluded"]["clicks"], 1.0)
        self.assertEqual(segments["non_branded"]["clicks"], 5.0)


class SitemapAnalyzerTests(unittest.TestCase):
    def test_valid_local_sitemap_with_inspection_passes(self) -> None:
        process = run(SITEMAP, "--sitemap", str(FIXTURES / "valid-sitemap.xml"), "--inspection", str(FIXTURES / "inspection.csv"), "--expected-host", "example.com", "--strict")
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(payload(process)["result"], "PASS")

    def test_missing_inspection_is_explicitly_incomplete(self) -> None:
        process = run(SITEMAP, "--sitemap", str(FIXTURES / "valid-sitemap.xml"), "--expected-host", "example.com", "--strict")
        self.assertEqual(process.returncode, 2)
        result = payload(process)
        self.assertEqual(result["result"], "INCOMPLETE")
        self.assertEqual(result["summary"]["inspection_evidence"], "unknown")

    def test_sitemap_index_reports_unaudited_children(self) -> None:
        process = run(SITEMAP, "--sitemap", str(FIXTURES / "sitemap-index.xml"), "--sitemap", str(FIXTURES / "valid-sitemap.xml"), "--inspection", str(FIXTURES / "inspection.csv"), "--expected-host", "example.com", "--strict")
        self.assertEqual(process.returncode, 2)
        result = payload(process)
        self.assertEqual(result["result"], "INCOMPLETE")
        self.assertEqual(result["summary"]["unaudited_index_child_count"], 1)

    def test_malformed_xml_and_missing_locations_fail(self) -> None:
        malformed = run(SITEMAP, "--sitemap", str(FIXTURES / "malformed.xml"), "--strict")
        missing_loc = run(SITEMAP, "--sitemap", str(FIXTURES / "missing-loc.xml"), "--strict")
        self.assertEqual(malformed.returncode, 2)
        self.assertEqual(payload(malformed)["result"], "FAIL")
        self.assertEqual(missing_loc.returncode, 2)
        self.assertEqual(payload(missing_loc)["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
