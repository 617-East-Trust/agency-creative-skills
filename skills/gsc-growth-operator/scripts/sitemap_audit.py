#!/usr/bin/env python3
"""Audit local XML sitemap files and optionally cross-reference URL Inspection CSV data."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def tag_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element if tag_name(child) == name]


def text_of(element: ET.Element, name: str) -> str:
    child = next((item for item in children(element, name)), None)
    return (child.text or "").strip() if child is not None else ""


def parse_lastmod(value: str) -> str | None:
    if not value:
        return None
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return None
    except ValueError:
        return "invalid"


def audit_sitemap(path: str) -> dict:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return {"file": path, "status": "invalid_xml", "error": str(exc), "urls": []}
    root_type = tag_name(root)
    if root_type == "urlset":
        urls = []
        for node in children(root, "url"):
            urls.append({"url": text_of(node, "loc"), "lastmod": text_of(node, "lastmod")})
        return {"file": path, "status": "ok", "type": "urlset", "urls": urls, "referenced_sitemaps": []}
    if root_type == "sitemapindex":
        refs = [text_of(node, "loc") for node in children(root, "sitemap")]
        return {"file": path, "status": "ok", "type": "sitemapindex", "urls": [], "referenced_sitemaps": refs}
    return {"file": path, "status": "unexpected_root", "type": root_type, "urls": [], "referenced_sitemaps": []}


def header_for(headers: list[str], options: list[str]) -> str | None:
    normalized = {header.lower().replace("_", " ").strip(): header for header in headers}
    for option in options:
        if option in normalized:
            return normalized[option]
    return None


def read_inspection(path: str) -> dict[str, dict[str, str]]:
    sample = Path(path).read_text(encoding="utf-8-sig")
    try:
        dialect = csv.Sniffer().sniff(sample[:8192], delimiters=",\t;")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(sample.splitlines(), dialect=dialect)
    if not reader.fieldnames:
        raise ValueError("inspection CSV has no header row")
    url_col = header_for(reader.fieldnames, ["url", "inspection url", "page"])
    if not url_col:
        raise ValueError("inspection CSV requires a url column")
    verdict_col = header_for(reader.fieldnames, ["verdict", "index verdict"])
    coverage_col = header_for(reader.fieldnames, ["coverage state", "coverage", "indexing state"])
    rows = {}
    for row in reader:
        url = (row.get(url_col) or "").strip()
        if url:
            rows[url] = {
                "verdict": (row.get(verdict_col) or "").strip() if verdict_col else "",
                "coverage_state": (row.get(coverage_col) or "").strip() if coverage_col else "",
            }
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sitemap", action="append", required=True, help="Local sitemap XML file; repeat for multiple files")
    parser.add_argument("--inspection", help="Optional URL Inspection CSV")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()
    try:
        files = [audit_sitemap(path) for path in args.sitemap]
        sitemap_urls = [row for file in files for row in file.get("urls", []) if row.get("url")]
        locations = [row["url"] for row in sitemap_urls]
        duplicates = [url for url, count in Counter(locations).items() if count > 1]
        hosts = Counter(urlparse(url).netloc.lower() for url in locations if urlparse(url).netloc)
        invalid_urls = [url for url in locations if urlparse(url).scheme not in {"http", "https"} or not urlparse(url).netloc]
        invalid_lastmod = [row["url"] for row in sitemap_urls if parse_lastmod(row.get("lastmod", ""))]
        future_lastmod = []
        now = datetime.now(timezone.utc)
        for row in sitemap_urls:
            value = row.get("lastmod", "")
            if not value or parse_lastmod(value):
                continue
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            if parsed > now:
                future_lastmod.append(row["url"])
        inspection = read_inspection(args.inspection) if args.inspection else {}
        inspections_in_sitemap = {url: inspection[url] for url in locations if url in inspection}
        not_indexed = {
            url: value
            for url, value in inspections_in_sitemap.items()
            if value["verdict"].lower() not in {"pass", "passed", ""}
            or any(word in value["coverage_state"].lower() for word in ("excluded", "not indexed", "crawled", "discovered"))
        }
        result = {
            "analysis": "sitemap_audit",
            "sitemap_files": [{key: value for key, value in file.items() if key != "urls"} for file in files],
            "summary": {
                "url_count": len(locations),
                "unique_url_count": len(set(locations)),
                "hosts": dict(hosts),
                "duplicate_url_count": len(duplicates),
                "invalid_url_count": len(invalid_urls),
                "invalid_lastmod_count": len(invalid_lastmod),
                "future_lastmod_count": len(future_lastmod),
                "inspection_rows": len(inspection),
                "inspection_matches": len(inspections_in_sitemap),
                "inspection_attention_count": len(not_indexed),
            },
            "duplicates": duplicates[:100],
            "invalid_urls": invalid_urls[:100],
            "invalid_lastmod": invalid_lastmod[:100],
            "future_lastmod": future_lastmod[:100],
            "inspection_attention": not_indexed,
            "notes": [
                "This validates provided sitemap files locally; it does not fetch URLs or establish Google indexation.",
                "A non-passing inspection state requires URL-level diagnosis using the indexing playbook.",
                "Keep only canonical, intended, 200, indexable URLs in production sitemaps.",
            ],
        }
        rendered = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
