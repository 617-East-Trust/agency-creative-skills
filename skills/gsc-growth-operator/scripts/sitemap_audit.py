#!/usr/bin/env python3
"""Audit local XML sitemap files and optionally cross-reference URL Inspection CSV data.

Network fetching is intentionally absent. Supply local sitemap/index files and any inspection
export explicitly. In --strict mode malformed input and un-audited index children fail.
"""

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
        return {"file": path, "status": "invalid_xml", "error": str(exc), "type": None, "urls": [], "referenced_sitemaps": [], "malformed_entries": []}
    root_type = tag_name(root)
    if root_type == "urlset":
        urls, malformed = [], []
        for index, node in enumerate(children(root, "url"), start=1):
            location = text_of(node, "loc")
            if not location:
                malformed.append({"entry": index, "reason": "missing_loc"})
            else:
                urls.append({"url": location, "lastmod": text_of(node, "lastmod")})
        return {"file": path, "status": "ok", "type": "urlset", "urls": urls, "referenced_sitemaps": [], "malformed_entries": malformed}
    if root_type == "sitemapindex":
        refs, malformed = [], []
        for index, node in enumerate(children(root, "sitemap"), start=1):
            location = text_of(node, "loc")
            if location:
                refs.append(location)
            else:
                malformed.append({"entry": index, "reason": "missing_loc"})
        return {"file": path, "status": "ok", "type": "sitemapindex", "urls": [], "referenced_sitemaps": refs, "malformed_entries": malformed}
    return {"file": path, "status": "unexpected_root", "type": root_type, "urls": [], "referenced_sitemaps": [], "malformed_entries": []}


def header_for(headers: list[str], options: list[str]) -> str | None:
    normalized = {header.lower().replace("_", " ").strip(): header for header in headers}
    for option in options:
        if option in normalized:
            return normalized[option]
    return None


def read_inspection(path: str) -> dict[str, dict[str, str]]:
    sample = Path(path).read_text(encoding="utf-8-sig")
    if not sample.strip():
        raise ValueError("inspection CSV is empty")
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
    rows: dict[str, dict[str, str]] = {}
    for row in reader:
        url = (row.get(url_col) or "").strip()
        if url:
            rows[url] = {
                "verdict": (row.get(verdict_col) or "").strip() if verdict_col else "",
                "coverage_state": (row.get(coverage_col) or "").strip() if coverage_col else "",
            }
    return rows


def status_for(files: list[dict], invalid_urls: list[str], invalid_lastmod: list[str], future_lastmod: list[str], host_mismatch: list[str], inspection_provided: bool, unaudited_children: list[str]) -> str:
    hard_failure = any(file["status"] != "ok" or file["malformed_entries"] for file in files) or bool(invalid_urls or invalid_lastmod or future_lastmod or host_mismatch)
    if hard_failure:
        return "FAIL"
    if not inspection_provided or unaudited_children:
        return "INCOMPLETE"
    return "PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sitemap", action="append", required=True, help="Local sitemap XML file; repeat for every index child to audit")
    parser.add_argument("--inspection", help="Optional URL Inspection CSV")
    parser.add_argument("--expected-host", help="Expected canonical hostname, e.g. www.example.com")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero for FAIL or INCOMPLETE outcomes")
    parser.add_argument("--output", help="Write JSON to this path instead of stdout")
    args = parser.parse_args()
    try:
        files = [audit_sitemap(path) for path in args.sitemap]
        sitemap_urls = [row for file in files for row in file["urls"]]
        locations = [row["url"] for row in sitemap_urls]
        duplicates = [url for url, count in Counter(locations).items() if count > 1]
        hosts = Counter(urlparse(url).netloc.lower() for url in locations if urlparse(url).netloc)
        invalid_urls = [url for url in locations if urlparse(url).scheme not in {"http", "https"} or not urlparse(url).netloc]
        expected_host = args.expected_host.lower() if args.expected_host else None
        host_mismatch = [url for url in locations if expected_host and urlparse(url).netloc.lower() != expected_host]
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
        inspection_state = "provided" if args.inspection else "unknown"
        referenced_children = [ref for file in files for ref in file["referenced_sitemaps"]]
        supplied_filenames = {Path(file["file"]).name for file in files}
        unaudited_children = [ref for ref in referenced_children if Path(urlparse(ref).path).name not in supplied_filenames]
        matched = {url: inspection[url] for url in locations if url in inspection}
        attention = {
            url: value
            for url, value in matched.items()
            if value["verdict"].lower() not in {"pass", "passed", ""}
            or any(token in value["coverage_state"].lower() for token in ("excluded", "not indexed", "crawled", "discovered"))
        }
        outcome = status_for(files, invalid_urls, invalid_lastmod, future_lastmod, host_mismatch, bool(args.inspection), unaudited_children)
        result = {
            "analysis": "sitemap_audit",
            "result": outcome,
            "sitemap_files": [{key: value for key, value in file.items() if key != "urls"} for file in files],
            "summary": {
                "url_count": len(locations),
                "unique_url_count": len(set(locations)),
                "hosts": dict(hosts),
                "expected_host": args.expected_host,
                "duplicate_url_count": len(duplicates),
                "invalid_url_count": len(invalid_urls),
                "host_mismatch_count": len(host_mismatch),
                "invalid_lastmod_count": len(invalid_lastmod),
                "future_lastmod_count": len(future_lastmod),
                "inspection_evidence": inspection_state,
                "inspection_rows": len(inspection),
                "inspection_matches": len(matched),
                "inspection_attention_count": len(attention),
                "unaudited_index_child_count": len(unaudited_children),
            },
            "duplicates": duplicates[:100],
            "invalid_urls": invalid_urls[:100],
            "host_mismatch": host_mismatch[:100],
            "invalid_lastmod": invalid_lastmod[:100],
            "future_lastmod": future_lastmod[:100],
            "unaudited_index_children": unaudited_children[:100],
            "inspection_attention": attention,
            "notes": [
                "Local sitemap validation does not fetch URLs or establish Google indexation.",
                "Inspection evidence is unknown when no inspection export is supplied.",
                "An index sitemap is incomplete until each child sitemap has been supplied and audited locally.",
            ],
        }
        rendered = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        else:
            print(rendered)
        if args.strict and outcome != "PASS":
            return 2
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
