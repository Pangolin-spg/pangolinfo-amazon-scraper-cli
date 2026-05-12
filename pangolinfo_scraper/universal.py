from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class UniversalScrapeBatchRequest:
    urls: List[str]
    format: str
    timeout_ms: Optional[int] = None

    def to_json(self) -> Dict[str, Any]:
        body: Dict[str, Any] = {"urls": self.urls, "format": self.format}
        if self.timeout_ms is not None:
            body["timeout"] = self.timeout_ms
        return body
