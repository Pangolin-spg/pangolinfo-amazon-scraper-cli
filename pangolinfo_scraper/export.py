from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def write_json(path: str, payload: Any) -> None:
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def extract_results_list(pangolinfo_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    data = pangolinfo_response.get("data")
    if not isinstance(data, dict):
        return []
    json_arr = data.get("json")
    if not isinstance(json_arr, list) or not json_arr:
        return []
    first = json_arr[0]
    if not isinstance(first, dict):
        return []
    inner_data = first.get("data")
    if not isinstance(inner_data, dict):
        return []
    results = inner_data.get("results")
    if not isinstance(results, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in results:
        if isinstance(item, dict):
            out.append(item)
    return out


def write_csv(path: str, rows: Iterable[Dict[str, Any]], *, columns: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            safe_row: Dict[str, Any] = {k: _to_scalar(row.get(k)) for k in columns}
            writer.writerow(safe_row)


def _to_scalar(v: Any) -> Any:
    if v is None:
        return ""
    if isinstance(v, (str, int, float)):
        return v
    return json.dumps(v, ensure_ascii=False)


def try_extract_universal_content(
    pangolinfo_response: Dict[str, Any], *, field: str
) -> Optional[str]:
    data = pangolinfo_response.get("data")
    if not isinstance(data, list) or not data:
        return None
    parts: List[str] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        content_list = item.get(field)
        if isinstance(content_list, list) and content_list:
            first = content_list[0]
            if isinstance(first, str) and first:
                parts.append(first)
    if not parts:
        return None
    return "\n\n".join(parts)
