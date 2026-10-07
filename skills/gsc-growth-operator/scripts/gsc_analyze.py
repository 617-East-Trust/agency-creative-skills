#!/usr/bin/env python3
"""Analyze Google Search Console CSV exports with no third-party dependencies."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

ALIASES = {
    "date": {"date", "day"},
    "query": {"query", "queries", "keyword", "keywords"},
    "page": {"page", "pages", "url", "landing page", "landing_page"},
    "clicks": {"clicks", "click"},
    "impressions": {"impressions", "impression", "impr"},
    "ctr": {"ctr", "click through rate", "click-through rate"},
    "position": {"position", "average position", "avg position", "avg_position"},
}


def normalized_key(key: str) -> str:
    return re.sub(r"[\s_\-]+", " ", key.strip().lower())


def source_column(headers: Iterable[str], field: str) -> str | None:
    wanted = {normalized_key(item) for item in ALIASES[field]}
    for header in headers:
        if normalized_key(header) in wanted:
            return header
    return None


def as_number(value: Any) -> float:
    if value in (None, ""):
        return 0.0
    raw = str(value).strip().replace(",", "")
    if raw.endswith("%"):
        return float(raw[:-1]) / 100
    return float(raw)


def as_date(value: str) -> str | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except ValueError:
        return value.strip()


def load_rows(path: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load a comma/tab/semicolon delimited GSC export into normalized records."""
    raw = Path(path).read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(raw[:8192], delimiters=",\t;")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(raw.splitlines(), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError(f"{path}: no header row found")
    columns = {field: source_column(reader.fieldnames, field) for field in ALIASES}
    required = [field for field in ("clicks", "impressions") if not columns[field]]
    if required:
        raise ValueError(f"{path}: required column(s) missing: {', '.join(required)}")
    rows: list[dict[str, Any]] = []
    for raw_row in reader:
        try:
            clicks = as_number(raw_row.get(columns["clicks"] or "", ""))
            impressions = as_number(raw_row.get(columns["impressions"] or "", ""))
            pos_value = raw_row.get(columns["position"] or "", "")
            position = as_number(pos_value) if pos_value not in (None, "") else None
        except ValueError as exc:
            raise ValueError(f"{path}: invalid numeric value in row {reader.line_num}: {exc}") from exc
        rows.append(
            {
                "date": as_date(raw_row.get(columns["date"] or "", "")),
                "query": (raw_row.get(columns["query"] or "", "") or "").strip(),
                "page": (raw_row.get(columns["page"] or "", "") or "").strip(),
                "clicks": clicks,
                "impressions": impressions,
                "position": position,
            }
        )
    dates = sorted({row["date"] for row in rows if row["date"]})
    return rows, {
        "file": str(path),
        "rows": len(rows),
        "columns": [field for field, source in columns.items() if source],
        "date_start": dates[0] if dates else None,
        "date_end": dates[-1] if dates else None,
    }


def aggregate(rows: Iterable[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(str(row.get(field, "") or "") for field in keys)
        bucket = buckets.setdefault(
            key,
            {**{field: value for field, value in zip(keys, key)}, "clicks": 0.0, "impressions": 0.0, "position_weight": 0.0, "position_impressions": 0.0},
        )
        bucket["clicks"] += row["clicks"]
        bucket["impressions"] += row["impressions"]
        if row["position"] is not None and row["impressions"] > 0:
            bucket["position_weight"] += row["position"] * row["impressions"]
            bucket["position_impressions"] += row["impressions"]
    output = []
    for bucket in buckets.values():
        bucket["ctr"] = bucket["clicks"] / bucket["impressions"] if bucket["impressions"] else 0.0
        bucket["position"] = (
            bucket["position_weight"] / bucket["position_impressions"] if bucket["position_impressions"] else None
        )
        del bucket["position_weight"], bucket["position_impressions"]
        output.append(bucket)
    return output


def round_metrics(item: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in item.items():
        if isinstance(value, float):
            result[key] = round(value, 4) if key in {"ctr", "position"} else round(value, 2)
        else:
            result[key] = value
    return result


def sort_rows(rows: list[dict[str, Any]], metric: str = "clicks", limit: int = 20) -> list[dict[str, Any]]:
    return [round_metrics(item) for item in sorted(rows, key=lambda row: row.get(metric, 0) or 0, reverse=True)[:limit]]


def overview(rows: list[dict[str, Any]], metadata: dict[str, Any], limit: int) -> dict[str, Any]:
    totals = aggregate(rows, tuple())[0] if rows else {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None}
    pages = aggregate((row for row in rows if row["page"]), ("page",))
    queries = aggregate((row for row in rows if row["query"]), ("query",))
    return {
        "analysis": "overview",
        "input": metadata,
        "totals": round_metrics(totals),
        "top_pages": sort_rows(pages, limit=limit),
        "top_queries": sort_rows(queries, limit=limit),
        "limitations": [
            "Results reflect only the export dimensions and filters.",
            "An absent URL or query in a performance export does not establish indexation status.",
        ],
    }


def key_label(row: dict[str, Any]) -> str:
    return row.get("page") or row.get("query") or "site total"


def comparison(current: list[dict[str, Any]], baseline: list[dict[str, Any]], current_meta: dict[str, Any], baseline_meta: dict[str, Any], limit: int, mode: str) -> dict[str, Any]:
    fields: tuple[str, ...]
    if any(row["page"] for row in current + baseline):
        fields = ("page", "query") if any(row["query"] for row in current + baseline) else ("page",)
    elif any(row["query"] for row in current + baseline):
        fields = ("query",)
    else:
        fields = tuple()
    current_groups = {tuple(row.get(field, "") for field in fields): row for row in aggregate(current, fields)}
    baseline_groups = {tuple(row.get(field, "") for field in fields): row for row in aggregate(baseline, fields)}
    entities = []
    for key in set(current_groups) | set(baseline_groups):
        cur = current_groups.get(key, {field: value for field, value in zip(fields, key)} | {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None})
        base = baseline_groups.get(key, {field: value for field, value in zip(fields, key)} | {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None})
        change = {field: cur.get(field, "") for field in fields}
        change.update(
            {
                "clicks_current": cur["clicks"],
                "clicks_baseline": base["clicks"],
                "clicks_delta": cur["clicks"] - base["clicks"],
                "impressions_current": cur["impressions"],
                "impressions_baseline": base["impressions"],
                "impressions_delta": cur["impressions"] - base["impressions"],
                "ctr_current": cur["ctr"],
                "ctr_baseline": base["ctr"],
                "ctr_delta": cur["ctr"] - base["ctr"],
                "position_current": cur["position"],
                "position_baseline": base["position"],
                "position_delta": (cur["position"] - base["position"] if cur["position"] is not None and base["position"] is not None else None),
            }
        )
        entities.append(change)
    total_current = aggregate(current, tuple())[0] if current else {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None}
    total_baseline = aggregate(baseline, tuple())[0] if baseline else {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None}
    key_metric = "clicks_delta" if mode == "compare" else "clicks_delta"
    sorted_entities = sorted(entities, key=lambda row: row[key_metric], reverse=(mode == "compare"))
    if mode in {"drops", "decay"}:
        sorted_entities = sorted(entities, key=lambda row: row["clicks_delta"])
    return {
        "analysis": mode,
        "current_input": current_meta,
        "baseline_input": baseline_meta,
        "scope": {"grain": list(fields) or ["site_total"]},
        "totals": {
            "current": round_metrics(total_current),
            "baseline": round_metrics(total_baseline),
            "clicks_delta": round(total_current["clicks"] - total_baseline["clicks"], 2),
            "impressions_delta": round(total_current["impressions"] - total_baseline["impressions"], 2),
        },
        "entities": [round_metrics(row) for row in sorted_entities[:limit]],
        "limitations": ["Confirm equal comparison windows and freshness before making causal claims."],
    }


def position_bucket(position: float | None) -> str:
    if position is None:
        return "unknown"
    if position <= 3:
        return "1-3"
    if position <= 10:
        return "4-10"
    if position <= 20:
        return "11-20"
    return "21+"


def ctr_opportunities(rows: list[dict[str, Any]], metadata: dict[str, Any], min_impressions: float, limit: int) -> dict[str, Any]:
    dims: tuple[str, ...] = ("page", "query") if any(row["page"] and row["query"] for row in rows) else (("page",) if any(row["page"] for row in rows) else ("query",))
    entities = aggregate(rows, dims)
    buckets: dict[str, dict[str, float]] = defaultdict(lambda: {"clicks": 0.0, "impressions": 0.0})
    for entity in entities:
        bucket = position_bucket(entity["position"])
        buckets[bucket]["clicks"] += entity["clicks"]
        buckets[bucket]["impressions"] += entity["impressions"]
    benchmark = {name: values["clicks"] / values["impressions"] if values["impressions"] else 0.0 for name, values in buckets.items()}
    candidates = []
    for entity in entities:
        bucket = position_bucket(entity["position"])
        expected_ctr = benchmark.get(bucket, 0.0)
        gap = max(0.0, expected_ctr - entity["ctr"])
        if entity["impressions"] >= min_impressions and gap > 0:
            candidate = dict(entity)
            candidate.update({"position_bucket": bucket, "benchmark_ctr": expected_ctr, "ctr_gap": gap, "estimated_click_gap": gap * entity["impressions"]})
            candidates.append(candidate)
    return {
        "analysis": "ctr_opportunities",
        "input": metadata,
        "minimum_impressions": min_impressions,
        "position_bucket_benchmarks": {key: round(value, 4) for key, value in benchmark.items()},
        "candidates": sort_rows(candidates, metric="estimated_click_gap", limit=limit),
        "limitations": [
            "Benchmarks are internal export averages, not universal expected CTRs.",
            "Validate SERP features, intent, brand effects, and page indexation before editing snippets.",
        ],
    }


def cannibalization(rows: list[dict[str, Any]], metadata: dict[str, Any], min_pages: int, min_impressions: float, limit: int) -> dict[str, Any]:
    if not any(row["query"] and row["page"] for row in rows):
        raise ValueError("cannibalization requires both query and page columns")
    pairs = aggregate((row for row in rows if row["query"] and row["page"]), ("query", "page"))
    queries: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for pair in pairs:
        queries[pair["query"]].append(pair)
    conflicts = []
    for query, pages in queries.items():
        material = [page for page in pages if page["impressions"] >= min_impressions]
        if len(material) >= min_pages:
            total = aggregate(material, tuple())[0]
            conflicts.append(
                {
                    "query": query,
                    "material_page_count": len(material),
                    "clicks": total["clicks"],
                    "impressions": total["impressions"],
                    "pages": sort_rows(material, limit=50),
                }
            )
    return {
        "analysis": "cannibalization_candidates",
        "input": metadata,
        "minimum_pages": min_pages,
        "minimum_impressions_per_page": min_impressions,
        "candidates": [round_metrics(item) for item in sorted(conflicts, key=lambda row: (row["material_page_count"], row["impressions"]), reverse=True)[:limit]],
        "limitations": ["Multiple ranking pages are candidates for review, not proof of harmful cannibalization."],
    }


def brand_split(rows: list[dict[str, Any]], metadata: dict[str, Any], terms: list[str]) -> dict[str, Any]:
    if not any(row["query"] for row in rows):
        raise ValueError("brand analysis requires a query column")
    patterns = [re.compile(r"(?<!\w)" + re.escape(term.strip().lower()) + r"(?!\w)") for term in terms if term.strip()]
    if not patterns:
        raise ValueError("at least one non-empty brand term is required")
    branded = [row for row in rows if any(pattern.search(row["query"].lower()) for pattern in patterns)]
    non_branded = [row for row in rows if row["query"] and row not in branded]
    unclassified = [row for row in rows if not row["query"]]
    return {
        "analysis": "brand_split",
        "input": metadata,
        "brand_terms": terms,
        "segments": {
            "branded": round_metrics(aggregate(branded, tuple())[0] if branded else {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None}),
            "non_branded": round_metrics(aggregate(non_branded, tuple())[0] if non_branded else {"clicks": 0.0, "impressions": 0.0, "ctr": 0.0, "position": None}),
            "unclassified_rows": len(unclassified),
        },
        "limitations": ["Review ambiguous brand/product terms and competitor names before publishing the split."],
    }


def new_keywords(current: list[dict[str, Any]], baseline: list[dict[str, Any]], current_meta: dict[str, Any], baseline_meta: dict[str, Any], limit: int) -> dict[str, Any]:
    if not any(row["query"] for row in current + baseline):
        raise ValueError("new-keywords requires a query column")
    current_queries = {row["query"]: row for row in aggregate((row for row in current if row["query"]), ("query",))}
    baseline_queries = {row["query"]: row for row in aggregate((row for row in baseline if row["query"]), ("query",))}
    found = []
    for query, row in current_queries.items():
        baseline_row = baseline_queries.get(query)
        if baseline_row is None or baseline_row["impressions"] == 0:
            found.append({**row, "baseline_impressions": 0.0, "baseline_clicks": 0.0})
    return {
        "analysis": "new_keywords",
        "current_input": current_meta,
        "baseline_input": baseline_meta,
        "queries": sort_rows(found, metric="impressions", limit=limit),
        "limitations": ["A query absent from an export may be omitted/anonymized rather than truly new."],
    }


def write_result(result: dict[str, Any], output: str | None) -> None:
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if output:
        Path(output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


def parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--limit", type=int, default=20, help="Maximum rows in ranked outputs (default: 20)")
    common.add_argument("--output", help="Write JSON to this path instead of stdout")
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("overview", "ctr", "cannibalization", "brand"):
        cmd = sub.add_parser(name, parents=[common])
        cmd.add_argument("--input", required=True, help="GSC CSV/TSV export")
        if name == "ctr":
            cmd.add_argument("--min-impressions", type=float, default=100)
        if name == "cannibalization":
            cmd.add_argument("--min-pages", type=int, default=2)
            cmd.add_argument("--min-impressions", type=float, default=20)
        if name == "brand":
            cmd.add_argument("--brand", required=True, help="Comma-separated confirmed brand terms")
    for name in ("compare", "drops", "decay", "new-keywords"):
        cmd = sub.add_parser(name, parents=[common])
        cmd.add_argument("--current", required=True, help="Current-period GSC CSV/TSV export")
        cmd.add_argument("--baseline", required=True, help="Equal-length prior-period GSC CSV/TSV export")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command in {"overview", "ctr", "cannibalization", "brand"}:
            rows, metadata = load_rows(args.input)
            if args.command == "overview":
                result = overview(rows, metadata, args.limit)
            elif args.command == "ctr":
                result = ctr_opportunities(rows, metadata, args.min_impressions, args.limit)
            elif args.command == "cannibalization":
                result = cannibalization(rows, metadata, args.min_pages, args.min_impressions, args.limit)
            else:
                result = brand_split(rows, metadata, [term.strip() for term in args.brand.split(",")])
        else:
            current, current_meta = load_rows(args.current)
            baseline, baseline_meta = load_rows(args.baseline)
            if args.command == "new-keywords":
                result = new_keywords(current, baseline, current_meta, baseline_meta, args.limit)
            else:
                result = comparison(current, baseline, current_meta, baseline_meta, args.limit, args.command)
        write_result(result, args.output)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
