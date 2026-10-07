#!/usr/bin/env python3
"""Validate and analyze Google Search Console CSV/TSV exports without third-party dependencies.

This utility analyzes the rows supplied to it. It does not claim property-level totals,
Google indexation status, or full query coverage unless a separate authoritative source is
provided. Use --property and --strict for repeatable client work.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit

ALIASES = {
    "date": {"date", "day"},
    "query": {"query", "queries", "keyword", "keywords"},
    "page": {"page", "pages", "url", "landing page", "landing_page"},
    "clicks": {"clicks", "click"},
    "impressions": {"impressions", "impression", "impr"},
    "ctr": {"ctr", "click through rate", "click-through rate"},
    "position": {"position", "average position", "avg position", "avg_position"},
    "country": {"country", "country code"},
    "device": {"device"},
    "search_type": {"search type", "search_type", "type"},
}
DIMENSIONS = ("date", "query", "page", "country", "device", "search_type")
METRICS = ("clicks", "impressions", "position")


def normalized_key(key: str) -> str:
    return re.sub(r"[\s_\-]+", " ", key.strip().lower())


def source_column(headers: Iterable[str], field: str) -> str | None:
    wanted = {normalized_key(item) for item in ALIASES[field]}
    for header in headers:
        if normalized_key(header) in wanted:
            return header
    return None


def parse_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValueError(f"{label}: invalid ISO date {value!r}") from exc


def parse_number(value: Any, label: str, *, allow_percent: bool = False, minimum: float = 0.0) -> float:
    if value is None or str(value).strip() == "":
        raise ValueError(f"{label}: missing numeric value")
    raw = str(value).strip().replace(",", "")
    if allow_percent and raw.endswith("%"):
        raw = raw[:-1]
        number = float(raw) / 100
    else:
        number = float(raw)
    if not math.isfinite(number):
        raise ValueError(f"{label}: non-finite numeric value {value!r}")
    if number < minimum:
        raise ValueError(f"{label}: value must be at least {minimum:g}, got {number:g}")
    return number


def normalize_url(value: str, mode: str) -> str:
    """Apply only an explicit, conservative URL normalization."""
    value = value.strip()
    if not value or mode == "none":
        return value
    parts = urlsplit(value)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        return value
    host = parts.hostname.lower() if parts.hostname else ""
    if parts.port and not ((parts.scheme == "http" and parts.port == 80) or (parts.scheme == "https" and parts.port == 443)):
        host = f"{host}:{parts.port}"
    path = parts.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    # Preserve query parameters and path case; both can be semantically meaningful.
    return urlunsplit((parts.scheme.lower(), host, path, parts.query, ""))


def empty_metrics() -> dict[str, Any]:
    return {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None}


def aggregate(rows: Iterable[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(str(row.get(field, "") or "") for field in keys)
        bucket = buckets.setdefault(
            key,
            {
                **{field: value for field, value in zip(keys, key)},
                "clicks": 0.0,
                "impressions": 0.0,
                "position_weight": 0.0,
                "position_impressions": 0.0,
            },
        )
        bucket["clicks"] += row["clicks"]
        bucket["impressions"] += row["impressions"]
        if row["position"] is not None and row["impressions"] > 0:
            bucket["position_weight"] += row["position"] * row["impressions"]
            bucket["position_impressions"] += row["impressions"]
    output = []
    for bucket in buckets.values():
        bucket["ctr"] = bucket["clicks"] / bucket["impressions"] if bucket["impressions"] else 0.0
        bucket["position"] = bucket["position_weight"] / bucket["position_impressions"] if bucket["position_impressions"] else None
        del bucket["position_weight"], bucket["position_impressions"]
        output.append(bucket)
    return output


def round_metrics(item: dict[str, Any]) -> dict[str, Any]:
    rounded: dict[str, Any] = {}
    for key, value in item.items():
        if isinstance(value, float):
            rounded[key] = round(value, 4) if any(token in key for token in ("ctr", "position", "relative")) else round(value, 2)
        elif isinstance(value, list):
            rounded[key] = [round_metrics(entry) if isinstance(entry, dict) else entry for entry in value]
        else:
            rounded[key] = value
    return rounded


def ranked(rows: Iterable[dict[str, Any]], metric: str, limit: int, reverse: bool = True) -> list[dict[str, Any]]:
    return [round_metrics(row) for row in sorted(rows, key=lambda row: (row.get(metric, 0) or 0, str(row)), reverse=reverse)[:limit]]


def options_from_args(args: argparse.Namespace) -> dict[str, Any]:
    as_of = parse_date(args.as_of_date, "--as-of-date") if args.as_of_date else date.today()
    if args.freshness_days < 0:
        raise ValueError("--freshness-days must be zero or greater")
    return {
        "property": args.property,
        "as_of": as_of,
        "freshness_days": args.freshness_days,
        "filters": {
            "country": args.country,
            "device": args.device,
            "search_type": args.search_type,
        },
        "normalize_urls": args.normalize_urls,
        "strict": args.strict,
    }


def read_export(path: str, options: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    raw = Path(path).read_text(encoding="utf-8-sig")
    if not raw.strip():
        raise ValueError(f"{path}: empty export")
    try:
        dialect = csv.Sniffer().sniff(raw[:8192], delimiters=",\t;")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(raw.splitlines(), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError(f"{path}: no header row found")
    columns = {field: source_column(reader.fieldnames, field) for field in ALIASES}
    missing = [field for field in ("clicks", "impressions") if not columns[field]]
    if missing:
        raise ValueError(f"{path}: required column(s) missing: {', '.join(missing)}")
    for filter_name, expected in options["filters"].items():
        if expected and not columns[filter_name]:
            raise ValueError(f"{path}: --{filter_name.replace('_', '-')} requires a matching column")

    rows: list[dict[str, Any]] = []
    warnings: list[str] = []
    invalid_or_missing_positions = 0
    freshness_excluded = 0
    filter_excluded = 0
    raw_count = 0
    cutoff = options["as_of"] - timedelta(days=options["freshness_days"])

    for source_row in reader:
        raw_count += 1
        label = f"{path}: row {reader.line_num}"
        raw_date = (source_row.get(columns["date"] or "", "") or "").strip()
        row_date = parse_date(raw_date, label) if raw_date else None
        try:
            clicks = parse_number(source_row.get(columns["clicks"] or ""), label + " clicks")
            impressions = parse_number(source_row.get(columns["impressions"] or ""), label + " impressions")
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        raw_position = source_row.get(columns["position"] or "", "") if columns["position"] else ""
        if raw_position is None or str(raw_position).strip() == "":
            position = None
            invalid_or_missing_positions += 1
        else:
            position = parse_number(raw_position, label + " position", minimum=0.000001)
        row: dict[str, Any] = {
            "date": row_date.isoformat() if row_date else None,
            "query": (source_row.get(columns["query"] or "", "") or "").strip(),
            "page": normalize_url((source_row.get(columns["page"] or "", "") or "").strip(), options["normalize_urls"]),
            "country": (source_row.get(columns["country"] or "", "") or "").strip(),
            "device": (source_row.get(columns["device"] or "", "") or "").strip(),
            "search_type": (source_row.get(columns["search_type"] or "", "") or "").strip(),
            "clicks": clicks,
            "impressions": impressions,
            "position": position,
        }
        if row_date and row_date > cutoff:
            freshness_excluded += 1
            continue
        if any(expected and row[field].casefold() != expected.casefold() for field, expected in options["filters"].items()):
            filter_excluded += 1
            continue
        rows.append(row)

    present_dimensions = [field for field in DIMENSIONS if columns[field]]
    blank_dimension_columns = [
        field for field in present_dimensions if any(not row[field] for row in rows) and any(row[field] for row in rows)
    ]
    if blank_dimension_columns:
        warnings.append("Mixed aggregation grain: populated and blank values in " + ", ".join(blank_dimension_columns))
    if not columns["date"]:
        warnings.append("No date dimension: freshness and comparison-window validation cannot be established from the export.")
    if not options["property"]:
        warnings.append("No --property supplied: output is not bound to a Search Console property identifier.")
    if invalid_or_missing_positions:
        warnings.append(f"{invalid_or_missing_positions} row(s) lack position and are excluded from position-normalized CTR checks.")

    exact_keys = [tuple(row[field] for field in DIMENSIONS) for row in rows]
    duplicate_count = sum(count - 1 for count in Counter(exact_keys).values() if count > 1)
    if duplicate_count:
        warnings.append(f"{duplicate_count} duplicate dimension row(s) detected; confirm export grain before relying on sums.")
    if options["strict"] and warnings:
        raise ValueError(f"{path}: strict validation failed: " + " | ".join(warnings))

    dates = sorted({row["date"] for row in rows if row["date"]})
    return rows, {
        "file": str(path),
        "rows_read": raw_count,
        "rows_after_filters": len(rows),
        "rows_excluded_by_freshness": freshness_excluded,
        "rows_excluded_by_dimension_filter": filter_excluded,
        "columns": [field for field, source in columns.items() if source],
        "aggregation_dimensions": present_dimensions,
        "date_start": dates[0] if dates else None,
        "date_end": dates[-1] if dates else None,
        "property": options["property"],
        "filters": {key: value for key, value in options["filters"].items() if value},
        "freshness": {"as_of": options["as_of"].isoformat(), "days": options["freshness_days"], "latest_included_date": cutoff.isoformat()},
        "url_normalization": options["normalize_urls"],
        "warnings": warnings,
    }


def date_span_days(metadata: dict[str, Any]) -> int | None:
    if not metadata["date_start"] or not metadata["date_end"]:
        return None
    return (parse_date(metadata["date_end"], "date_end") - parse_date(metadata["date_start"], "date_start")).days + 1


def validate_periods(current_meta: dict[str, Any], baseline_meta: dict[str, Any], strict: bool, *, decay_days: int | None = None) -> dict[str, Any]:
    current_days, baseline_days = date_span_days(current_meta), date_span_days(baseline_meta)
    validation = {"status": "validated", "current_days": current_days, "baseline_days": baseline_days, "checks": []}
    if current_days is None or baseline_days is None:
        message = "Comparison windows are unvalidated because one or both exports lack a date dimension."
        if strict:
            raise ValueError(message)
        return {**validation, "status": "unvalidated", "checks": [message]}
    if current_days != baseline_days:
        raise ValueError(f"Comparison windows must be equal length; current={current_days} days, baseline={baseline_days} days.")
    if parse_date(baseline_meta["date_end"], "baseline date_end") >= parse_date(current_meta["date_start"], "current date_start"):
        raise ValueError("Comparison windows must not overlap.")
    if current_meta["filters"] != baseline_meta["filters"]:
        raise ValueError("Comparison exports have incompatible dimension filters.")
    if current_meta["property"] and baseline_meta["property"] and current_meta["property"] != baseline_meta["property"]:
        raise ValueError("Comparison exports identify different --property values.")
    if current_meta["aggregation_dimensions"] != baseline_meta["aggregation_dimensions"]:
        raise ValueError("Comparison exports have incompatible aggregation dimensions.")
    if decay_days and (current_days != decay_days or baseline_days != decay_days):
        raise ValueError(f"Decay analysis requires two {decay_days}-day windows; received {current_days} and {baseline_days} days.")
    validation["checks"] = ["equal non-overlapping dated windows", "matching explicit filters"]
    if decay_days:
        validation["checks"].append(f"two {decay_days}-day windows")
    return validation


def overview(rows: list[dict[str, Any]], metadata: dict[str, Any], limit: int) -> dict[str, Any]:
    export_totals = aggregate(rows, tuple())[0] if rows else empty_metrics()
    pages = aggregate((row for row in rows if row["page"]), ("page",))
    queries = aggregate((row for row in rows if row["query"]), ("query",))
    aggregation_type = " × ".join(metadata["aggregation_dimensions"]) or "metrics-only export"
    return {
        "analysis": "overview",
        "input": metadata,
        "export_totals": round_metrics(export_totals),
        "property_totals": None,
        "aggregation_type": aggregation_type,
        "query_coverage": "partial_or_unknown" if "query" in metadata["aggregation_dimensions"] else "not_supplied",
        "known_truncation": "Detailed query/page export rows can omit anonymized data or be limited by the source export. Do not treat export_totals as authoritative property totals.",
        "top_pages": ranked(pages, "clicks", limit),
        "top_queries": ranked(queries, "clicks", limit),
    }


def entity_dimensions(current: list[dict[str, Any]], baseline: list[dict[str, Any]]) -> tuple[str, ...]:
    all_rows = current + baseline
    if any(row["page"] for row in all_rows):
        return ("page", "query") if any(row["query"] for row in all_rows) else ("page",)
    if any(row["query"] for row in all_rows):
        return ("query",)
    return tuple()


def comparison(current: list[dict[str, Any]], baseline: list[dict[str, Any]], current_meta: dict[str, Any], baseline_meta: dict[str, Any], limit: int, mode: str, strict: bool, *, min_click_loss: float = 1.0, min_relative_loss: float = 0.0, decay_days: int | None = None) -> dict[str, Any]:
    validation = validate_periods(current_meta, baseline_meta, strict, decay_days=decay_days)
    dimensions = entity_dimensions(current, baseline)
    current_groups = {tuple(row.get(field, "") for field in dimensions): row for row in aggregate(current, dimensions)}
    baseline_groups = {tuple(row.get(field, "") for field in dimensions): row for row in aggregate(baseline, dimensions)}
    entities = []
    for key in set(current_groups) | set(baseline_groups):
        cur = current_groups.get(key, {field: value for field, value in zip(dimensions, key)} | empty_metrics())
        base = baseline_groups.get(key, {field: value for field, value in zip(dimensions, key)} | empty_metrics())
        clicks_delta = cur["clicks"] - base["clicks"]
        relative_delta = clicks_delta / base["clicks"] if base["clicks"] else None
        entities.append(
            {
                **{field: cur.get(field, "") or base.get(field, "") for field in dimensions},
                "clicks_current": cur["clicks"],
                "clicks_baseline": base["clicks"],
                "clicks_delta": clicks_delta,
                "relative_clicks_delta": relative_delta,
                "impressions_current": cur["impressions"],
                "impressions_baseline": base["impressions"],
                "impressions_delta": cur["impressions"] - base["impressions"],
                "ctr_current": cur["ctr"],
                "ctr_baseline": base["ctr"],
                "ctr_delta": cur["ctr"] - base["ctr"],
                "position_current": cur["position"],
                "position_baseline": base["position"],
                "position_delta": cur["position"] - base["position"] if cur["position"] is not None and base["position"] is not None else None,
            }
        )
    total_current = aggregate(current, tuple())[0] if current else empty_metrics()
    total_baseline = aggregate(baseline, tuple())[0] if baseline else empty_metrics()
    base = {
        "analysis": mode,
        "current_input": current_meta,
        "baseline_input": baseline_meta,
        "period_validation": validation,
        "scope": {"grain": list(dimensions) or ["site_total"]},
        "export_totals": {
            "current": round_metrics(total_current),
            "baseline": round_metrics(total_baseline),
            "clicks_delta": round(total_current["clicks"] - total_baseline["clicks"], 2),
            "impressions_delta": round(total_current["impressions"] - total_baseline["impressions"], 2),
        },
        "property_totals": None,
    }
    if mode == "compare":
        return base | {
            "gainers": ranked((row for row in entities if row["clicks_delta"] > 0), "clicks_delta", limit),
            "losers": ranked((row for row in entities if row["clicks_delta"] < 0), "clicks_delta", limit, reverse=False),
        }
    losses = [
        row
        for row in entities
        if row["clicks_delta"] <= -min_click_loss
        and (row["relative_clicks_delta"] is None or row["relative_clicks_delta"] <= -min_relative_loss)
    ]
    return base | {
        "minimum_click_loss": min_click_loss,
        "minimum_relative_click_loss": min_relative_loss,
        "candidates": ranked(losses, "clicks_delta", limit, reverse=False),
        "limitations": [
            "Candidates are export-level declines, not causal diagnoses.",
            "For decay, two windows screen for a sustained-period candidate; confirm intent, seasonality, release history, and indexation before action.",
        ],
    }


def position_bucket(position: float | None) -> str | None:
    if position is None:
        return None
    if position <= 3:
        return "1-3"
    if position <= 10:
        return "4-10"
    if position <= 20:
        return "11-20"
    return "21+"


def read_ctr_benchmark(path: str) -> dict[str, float]:
    raw = Path(path).read_text(encoding="utf-8-sig")
    reader = csv.DictReader(raw.splitlines())
    if not reader.fieldnames:
        raise ValueError("CTR benchmark file has no header row")
    bucket_col = source_column(reader.fieldnames, "position") or next((item for item in reader.fieldnames if normalized_key(item) == "position bucket"), None)
    ctr_col = source_column(reader.fieldnames, "ctr") or next((item for item in reader.fieldnames if normalized_key(item) == "expected ctr"), None)
    if not bucket_col or not ctr_col:
        raise ValueError("CTR benchmark requires position_bucket (or position) and expected_ctr (or ctr) columns")
    result = {}
    for index, row in enumerate(reader, start=2):
        bucket = (row.get(bucket_col) or "").strip()
        if bucket:
            result[bucket] = parse_number(row.get(ctr_col), f"benchmark row {index} expected CTR", allow_percent=True)
    if not result:
        raise ValueError("CTR benchmark has no usable rows")
    return result


def ctr_screen(rows: list[dict[str, Any]], metadata: dict[str, Any], min_impressions: float, min_cohort_size: int, limit: int, benchmark_path: str | None) -> dict[str, Any]:
    dimensions = ("page", "query") if any(row["page"] and row["query"] for row in rows) else (("page",) if any(row["page"] for row in rows) else ("query",))
    entities = aggregate(rows, dimensions)
    positioned = [row for row in entities if position_bucket(row["position"]) is not None]
    cohorts: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entity in positioned:
        cohorts[position_bucket(entity["position"]) or "unknown"].append(entity)
    benchmark = read_ctr_benchmark(benchmark_path) if benchmark_path else None
    cohort_metadata = {
        bucket: {"entity_count": len(items), "impressions": round(sum(item["impressions"] for item in items), 2)}
        for bucket, items in cohorts.items()
    }
    candidates = []
    screen = []
    for entity in positioned:
        bucket = position_bucket(entity["position"]) or "unknown"
        if entity["impressions"] < min_impressions or len(cohorts[bucket]) < min_cohort_size:
            continue
        record = dict(entity) | {"position_bucket": bucket, "cohort_size": len(cohorts[bucket])}
        if benchmark and bucket in benchmark:
            expected_ctr = benchmark[bucket]
            gap = max(0.0, expected_ctr - entity["ctr"])
            if gap > 0:
                candidates.append(record | {"benchmark_ctr": expected_ctr, "ctr_gap": gap, "estimated_click_gap": gap * entity["impressions"]})
        else:
            screen.append(record)
    return {
        "analysis": "ctr_opportunities" if benchmark else "ctr_screen",
        "input": metadata,
        "minimum_impressions": min_impressions,
        "minimum_cohort_size": min_cohort_size,
        "cohorts": cohort_metadata,
        "benchmark_source": benchmark_path or None,
        "candidates": ranked(candidates if benchmark else screen, "estimated_click_gap" if benchmark else "impressions", limit),
        "excluded_missing_position_entity_count": len(entities) - len(positioned),
        "limitations": [
            "Without an explicit external CTR benchmark, this is a position-filtered screening list, not an expected-CTR opportunity calculation.",
            "Validate SERP features, intent, brand effects, and page indexation before editing snippets.",
        ],
    }


def cannibalization(rows: list[dict[str, Any]], metadata: dict[str, Any], min_pages: int, min_impressions: float, limit: int) -> dict[str, Any]:
    if not any(row["query"] and row["page"] for row in rows):
        raise ValueError("cannibalization requires both query and page columns")
    pairs = aggregate((row for row in rows if row["query"] and row["page"]), ("query", "page"))
    by_query: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pair in pairs:
        by_query[pair["query"]].append(pair)
    candidates = []
    for query, pages in by_query.items():
        material = [page for page in pages if page["impressions"] >= min_impressions]
        if len(material) >= min_pages:
            total = aggregate(material, tuple())[0]
            candidates.append({"query": query, "material_page_count": len(material), "clicks": total["clicks"], "impressions": total["impressions"], "pages": ranked(material, "clicks", 50)})
    return {
        "analysis": "cannibalization_candidates",
        "input": metadata,
        "minimum_pages": min_pages,
        "minimum_impressions_per_page": min_impressions,
        "candidates": ranked(candidates, "impressions", limit),
        "limitations": ["Multiple ranking pages are review candidates, not proof of harmful cannibalization."],
    }


def patterns(terms: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(r"(?<!\w)" + re.escape(term.strip().casefold()) + r"(?!\w)") for term in terms if term.strip()]


def brand_split(rows: list[dict[str, Any]], metadata: dict[str, Any], brand_terms: list[str], ambiguous_terms: list[str], excluded_terms: list[str]) -> dict[str, Any]:
    if not any(row["query"] for row in rows):
        raise ValueError("brand analysis requires a query column")
    brand_patterns, ambiguous_patterns, excluded_patterns = patterns(brand_terms), patterns(ambiguous_terms), patterns(excluded_terms)
    if not brand_patterns:
        raise ValueError("at least one --brand term is required")
    segments: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        query = row["query"].casefold()
        if not query:
            segments["unclassified"].append(row)
        elif any(pattern.search(query) for pattern in excluded_patterns):
            segments["excluded"].append(row)
        elif any(pattern.search(query) for pattern in ambiguous_patterns):
            segments["ambiguous"].append(row)
        elif any(pattern.search(query) for pattern in brand_patterns):
            segments["branded"].append(row)
        else:
            segments["non_branded"].append(row)
    return {
        "analysis": "brand_split",
        "input": metadata,
        "classification_terms": {"brand": brand_terms, "ambiguous": ambiguous_terms, "exclude": excluded_terms},
        "segments": {name: round_metrics(aggregate(entries, tuple())[0] if entries else empty_metrics()) for name, entries in ((name, segments[name]) for name in ("branded", "non_branded", "ambiguous", "excluded", "unclassified"))},
        "limitations": ["Review the supplied brand, ambiguous, and excluded terms before publishing the split."],
    }


def new_keywords(current: list[dict[str, Any]], baseline: list[dict[str, Any]], current_meta: dict[str, Any], baseline_meta: dict[str, Any], limit: int, strict: bool, min_impressions: float, min_clicks: float) -> dict[str, Any]:
    validation = validate_periods(current_meta, baseline_meta, strict)
    if not any(row["query"] for row in current + baseline):
        raise ValueError("new-keywords requires a query column")
    current_queries = {row["query"]: row for row in aggregate((row for row in current if row["query"]), ("query",))}
    baseline_queries = {row["query"]: row for row in aggregate((row for row in baseline if row["query"]), ("query",))}
    candidates = [
        row | {"baseline_impressions": 0.0, "baseline_clicks": 0.0}
        for query, row in current_queries.items()
        if query not in baseline_queries and row["impressions"] >= min_impressions and row["clicks"] >= min_clicks
    ]
    return {
        "analysis": "new_keywords",
        "current_input": current_meta,
        "baseline_input": baseline_meta,
        "period_validation": validation,
        "minimum_impressions": min_impressions,
        "minimum_clicks": min_clicks,
        "queries": ranked(candidates, "impressions", limit),
        "limitations": ["A query absent from an export may be anonymized or omitted rather than truly new."],
    }


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=20, help="Maximum rows in ranked output (default: 20)")
    parser.add_argument("--output", help="Write JSON to this path instead of stdout")
    parser.add_argument("--property", help="Search Console property identifier, e.g. sc-domain:example.com")
    parser.add_argument("--as-of-date", help="Analysis date for reproducible freshness filtering (YYYY-MM-DD; default: today)")
    parser.add_argument("--freshness-days", type=int, default=3, help="Exclude dated rows newer than as-of minus this many calendar days (default: 3)")
    parser.add_argument("--country", help="Keep only this country value when the export has a country column")
    parser.add_argument("--device", help="Keep only this device value when the export has a device column")
    parser.add_argument("--search-type", help="Keep only this search type when the export has a search-type column")
    parser.add_argument("--normalize-urls", choices=("none", "safe"), default="none", help="Explicitly normalize safe URL variants; default preserves export URLs")
    parser.add_argument("--strict", action="store_true", help="Fail on missing property/date context, mixed grain, or duplicate dimension rows")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("overview", "ctr", "cannibalization", "brand"):
        command = sub.add_parser(name)
        add_common_arguments(command)
        command.add_argument("--input", required=True, help="GSC CSV/TSV export")
        if name == "ctr":
            command.add_argument("--min-impressions", type=float, default=100)
            command.add_argument("--min-cohort-size", type=int, default=5)
            command.add_argument("--benchmark", help="Optional CSV with position_bucket and expected_ctr; required for numeric click-gap estimates")
        if name == "cannibalization":
            command.add_argument("--min-pages", type=int, default=2)
            command.add_argument("--min-impressions", type=float, default=20)
        if name == "brand":
            command.add_argument("--brand", required=True, help="Comma-separated confirmed brand terms")
            command.add_argument("--ambiguous", default="", help="Comma-separated terms that require manual review")
            command.add_argument("--exclude", default="", help="Comma-separated terms to remove from the brand/non-brand comparison")
    for name in ("compare", "drops", "decay", "new-keywords"):
        command = sub.add_parser(name)
        add_common_arguments(command)
        command.add_argument("--current", required=True, help="Current-period GSC CSV/TSV export")
        command.add_argument("--baseline", required=True, help="Equal-length prior-period GSC CSV/TSV export")
        if name in {"drops", "decay"}:
            command.add_argument("--min-click-loss", type=float, default=1.0)
            command.add_argument("--min-relative-click-loss", type=float, default=0.0)
        if name == "decay":
            command.add_argument("--lookback-days", type=int, default=90)
        if name == "new-keywords":
            command.add_argument("--min-impressions", type=float, default=10)
            command.add_argument("--min-clicks", type=float, default=0)
    return root


def write_result(result: dict[str, Any], output: str | None) -> None:
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if output:
        Path(output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def main() -> int:
    args = parser().parse_args()
    try:
        options = options_from_args(args)
        if args.command in {"overview", "ctr", "cannibalization", "brand"}:
            rows, metadata = read_export(args.input, options)
            if args.command == "overview":
                result = overview(rows, metadata, args.limit)
            elif args.command == "ctr":
                result = ctr_screen(rows, metadata, args.min_impressions, args.min_cohort_size, args.limit, args.benchmark)
            elif args.command == "cannibalization":
                result = cannibalization(rows, metadata, args.min_pages, args.min_impressions, args.limit)
            else:
                split = lambda value: [term.strip() for term in value.split(",") if term.strip()]
                result = brand_split(rows, metadata, split(args.brand), split(args.ambiguous), split(args.exclude))
        else:
            current, current_meta = read_export(args.current, options)
            baseline, baseline_meta = read_export(args.baseline, options)
            if args.command == "compare":
                result = comparison(current, baseline, current_meta, baseline_meta, args.limit, "compare", args.strict)
            elif args.command == "drops":
                result = comparison(current, baseline, current_meta, baseline_meta, args.limit, "drops", args.strict, min_click_loss=args.min_click_loss, min_relative_loss=args.min_relative_click_loss)
            elif args.command == "decay":
                result = comparison(current, baseline, current_meta, baseline_meta, args.limit, "decay_candidates", args.strict, min_click_loss=args.min_click_loss, min_relative_loss=args.min_relative_click_loss, decay_days=args.lookback_days)
            else:
                result = new_keywords(current, baseline, current_meta, baseline_meta, args.limit, args.strict, args.min_impressions, args.min_clicks)
        write_result(result, args.output)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
