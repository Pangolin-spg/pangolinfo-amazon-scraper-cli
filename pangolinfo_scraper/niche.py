from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class CategoryChildrenRequest:
    parent_browse_node_id_path: str
    page: int = 1
    size: int = 10

    def to_json(self) -> Dict[str, Any]:
        return {
            "parentBrowseNodeIdPath": self.parent_browse_node_id_path,
            "page": self.page,
            "size": self.size,
        }


@dataclass(frozen=True)
class CategorySearchRequest:
    keyword: str
    page: int = 1
    size: int = 10

    def to_json(self) -> Dict[str, Any]:
        return {"keyword": self.keyword, "page": self.page, "size": self.size}


@dataclass(frozen=True)
class CategoryPathsRequest:
    category_ids: List[str]

    def to_json(self) -> Dict[str, Any]:
        return {"categoryIds": self.category_ids}


@dataclass(frozen=True)
class CategoryFilterRequest:
    marketplace_id: str
    time_range: str
    sample_scope: str
    category_id: Optional[str]
    page: int = 1
    size: int = 10
    sort_field: Optional[str] = None
    sort_order: Optional[str] = None

    def to_json(self) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "marketplaceId": self.marketplace_id,
            "timeRange": self.time_range,
            "sampleScope": self.sample_scope,
            "page": self.page,
            "size": self.size,
        }
        if self.category_id is not None:
            body["categoryId"] = self.category_id
        if self.sort_field is not None:
            body["sortField"] = self.sort_field
        if self.sort_order is not None:
            body["sortOrder"] = self.sort_order
        return body


@dataclass(frozen=True)
class NicheFilterRequest:
    marketplace_id: str
    niche_id: Optional[str] = None
    niche_title: Optional[str] = None
    page: int = 1
    size: int = 10
    sort_field: Optional[str] = None
    sort_order: Optional[str] = None

    def to_json(self) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "marketplaceId": self.marketplace_id,
            "page": self.page,
            "size": self.size,
        }
        if self.niche_id is not None:
            body["nicheId"] = self.niche_id
        if self.niche_title is not None:
            body["nicheTitle"] = self.niche_title
        if self.sort_field is not None:
            body["sortField"] = self.sort_field
        if self.sort_order is not None:
            body["sortOrder"] = self.sort_order
        return body
