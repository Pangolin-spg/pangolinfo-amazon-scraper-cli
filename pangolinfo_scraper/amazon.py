from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class AmazonScrapeRequest:
    url: Optional[str]
    parser_name: str
    site: str
    content: str
    format: str
    biz_context: Dict[str, Any]

    def to_json(self) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "parserName": self.parser_name,
            "site": self.site,
            "content": self.content,
            "format": self.format,
            "bizContext": self.biz_context,
        }
        if self.url is not None:
            body["url"] = self.url
        return body


def build_product_detail_request(
    *,
    asin: Optional[str],
    url: Optional[str],
    site: str,
    zipcode: Optional[str],
    format: str,
) -> AmazonScrapeRequest:
    biz_context: Dict[str, Any] = {}
    if zipcode is not None:
        biz_context["zipcode"] = zipcode
    return AmazonScrapeRequest(
        url=url,
        parser_name="amzProductDetail",
        site=site,
        content=asin or "",
        format=format,
        biz_context=biz_context,
    )


def build_keyword_request(
    *,
    keyword: str,
    url: Optional[str],
    site: str,
    zipcode: Optional[str],
    format: str,
) -> AmazonScrapeRequest:
    biz_context: Dict[str, Any] = {}
    if zipcode is not None:
        biz_context["zipcode"] = zipcode
    return AmazonScrapeRequest(
        url=url,
        parser_name="amzKeyword",
        site=site,
        content=keyword,
        format=format,
        biz_context=biz_context,
    )


def build_category_products_request(
    *,
    category_node_id: str,
    url: Optional[str],
    site: str,
    zipcode: Optional[str],
    format: str,
) -> AmazonScrapeRequest:
    biz_context: Dict[str, Any] = {}
    if zipcode is not None:
        biz_context["zipcode"] = zipcode
    return AmazonScrapeRequest(
        url=url,
        parser_name="amzProductOfCategory",
        site=site,
        content=category_node_id,
        format=format,
        biz_context=biz_context,
    )


def build_seller_products_request(
    *,
    seller_id: str,
    url: Optional[str],
    site: str,
    zipcode: Optional[str],
    format: str,
) -> AmazonScrapeRequest:
    biz_context: Dict[str, Any] = {}
    if zipcode is not None:
        biz_context["zipcode"] = zipcode
    return AmazonScrapeRequest(
        url=url,
        parser_name="amzProductOfSeller",
        site=site,
        content=seller_id,
        format=format,
        biz_context=biz_context,
    )


def build_best_sellers_request(
    *,
    best_sellers_keyword: str,
    url: Optional[str],
    site: str,
    zipcode: Optional[str],
    format: str,
) -> AmazonScrapeRequest:
    biz_context: Dict[str, Any] = {}
    if zipcode is not None:
        biz_context["zipcode"] = zipcode
    return AmazonScrapeRequest(
        url=url,
        parser_name="amzBestSellers",
        site=site,
        content=best_sellers_keyword,
        format=format,
        biz_context=biz_context,
    )


def build_new_releases_request(
    *,
    new_releases_keyword: str,
    url: Optional[str],
    site: str,
    zipcode: Optional[str],
    format: str,
) -> AmazonScrapeRequest:
    biz_context: Dict[str, Any] = {}
    if zipcode is not None:
        biz_context["zipcode"] = zipcode
    return AmazonScrapeRequest(
        url=url,
        parser_name="amzNewReleases",
        site=site,
        content=new_releases_keyword,
        format=format,
        biz_context=biz_context,
    )


def build_reviews_request(
    *,
    asin: str,
    site: str,
    page_count: int,
    filter_by_star: str,
    sort_by: str,
    format: str,
    format_type: str,
    media_type: str,
    url: str = "https://www.amazon.com",
) -> Dict[str, Any]:
    return {
        "url": url,
        "site": site,
        "format": format,
        "formatType": format_type,
        "mediaType": media_type,
        "parserName": "amzReviewV2",
        "bizContext": {
            "bizKey": "review",
            "pageCount": page_count,
            "asin": asin,
            "filterByStar": filter_by_star,
            "sortBy": sort_by,
        },
    }
