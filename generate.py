#!/usr/bin/env python3
"""
Generate index.html (Obtainium import links page) from config.ini.
Only uses the Python standard library (configparser, json, urllib) -
no pip install needed.

Usage:
    python generate.py [config_path] [output_path]

Defaults:
    config_path = ./config.ini
    output_path = ./index.html
"""
import configparser
import json
import sys
import urllib.parse
from collections import OrderedDict
from pathlib import Path

REDIRECT_BASE = "https://apps.obtainium.imranr.dev/redirect?r="

# Keys that map directly onto the outer Obtainium JSON object,
# instead of going into "additionalSettings".
CORE_KEYS = {
    "group", "label", "id", "url", "author", "name",
    "preferredapkindex", "overridesource",
}


def parse_value(raw: str):
    """Turn an ini string into bool / int / str as appropriate."""
    low = raw.strip().lower()
    if low in ("true", "false"):
        return low == "true"
    if raw.strip().lstrip("-").isdigit():
        return int(raw.strip())
    return raw


def build_link(item: dict) -> str:
    payload = {
        "id": item["id"],
        "url": item["url"],
        "author": item.get("author", ""),
        "name": item.get("name", ""),
    }
    if "preferredapkindex" in item:
        payload["preferredApkIndex"] = parse_value(item["preferredapkindex"])

    additional = {
        k: parse_value(v)
        for k, v in item.items()
        if k not in CORE_KEYS
    }
    if additional:
        payload["additionalSettings"] = json.dumps(
            additional, separators=(",", ":"), ensure_ascii=False
        )

    if "overridesource" in item:
        payload["overrideSource"] = item["overridesource"]

    json_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    encoded_json = urllib.parse.quote(json_str, safe="")
    return f"{REDIRECT_BASE}obtainium://app/{encoded_json}"


def render_group(title: str, items: list) -> str:
    cols = len(items)
    header = (
        '  <tr>\n'
        f'    <td style="font-size: 33px; text-align: center; vertical-align: middle;" colspan="{cols}">{title}</td>\n'
        '  </tr>'
    )
    cells = []
    for item in items:
        href = build_link(item)
        label = item["label"]
        cells.append(
            '    <td style="font-size: 31px; text-align: center; vertical-align: middle;">\n'
            f'      <a href="{href}"><ins><code>{label}</code></ins></a>\n'
            '    </td>'
        )
    row = "  <tr>\n" + "\n".join(cells) + "\n  </tr>"
    return f'<table border="1" cellpadding="6">\n{header}\n{row}\n</table>'


def main():
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config.ini")
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("index.html")

    parser = configparser.ConfigParser()
    parser.optionxform = str  # preserve key case (e.g. apkFilterRegEx)
    parser.read(config_path, encoding="utf-8")

    page_title = "Import Links cho Obtainium"
    if parser.has_section("title") and parser.has_option("title", "page_title"):
        page_title = parser.get("title", "page_title")

    # Group app sections by their "group" value, preserving file order.
    groups = OrderedDict()
    for section in parser.sections():
        if section == "title":
            continue
        item = {k.lower() if k.lower() in CORE_KEYS else k: v
                for k, v in parser.items(section)}
        group_title = item.get("group", "Ungrouped")
        groups.setdefault(group_title, []).append(item)

    groups_html = "\n\n<br>\n\n".join(
        render_group(title, items) for title, items in groups.items()
    )

    html = (
        '<div align="center">\n'
        f'<h2>{page_title}</h2>\n\n'
        f'{groups_html}\n'
        '</div>\n'
    )

    output_path.write_text(html, encoding="utf-8")
    print(f"Generated {output_path} from {config_path} ({len(groups)} groups, "
          f"{sum(len(v) for v in groups.values())} links)")


if __name__ == "__main__":
    main()
