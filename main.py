import json
import os
from typing import Optional

import click

from pangolinfo_scraper.amazon import (
    build_best_sellers_request,
    build_category_products_request,
    build_keyword_request,
    build_new_releases_request,
    build_product_detail_request,
    build_reviews_request,
    build_seller_products_request,
)
from pangolinfo_scraper.client import PangolinfoClient, PangolinfoError
from pangolinfo_scraper.export import (
    extract_results_list,
    try_extract_universal_content,
    write_csv,
    write_json,
    write_text,
)
from pangolinfo_scraper.niche import (
    CategoryChildrenRequest,
    CategoryFilterRequest,
    CategoryPathsRequest,
    CategorySearchRequest,
    NicheFilterRequest,
)
from pangolinfo_scraper.universal import UniversalScrapeBatchRequest


def _resolve_token(
    client: PangolinfoClient,
    *,
    token: Optional[str],
    email: Optional[str],
    password: Optional[str],
    dry_run: bool,
) -> str:
    if token:
        return token
    if dry_run:
        return "<dry-run-token>"
    if email and password:
        return client.auth(email=email, password=password)
    raise click.ClickException(
        "Missing credentials. Provide --token / PANGOLINFO_TOKEN, or --email+--password / PANGOLINFO_EMAIL+PANGOLINFO_PASSWORD."
    )


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--base-url", default="https://scrapeapi.pangolinfo.com", show_default=True)
@click.option("--token", default=lambda: os.getenv("PANGOLINFO_TOKEN"))
@click.option("--email", default=lambda: os.getenv("PANGOLINFO_EMAIL"))
@click.option("--password", default=lambda: os.getenv("PANGOLINFO_PASSWORD"))
@click.option("--dry-run", is_flag=True, help="Print request JSON without sending it.")
@click.pass_context
def cli(ctx, base_url, token, email, password, dry_run):
    ctx.obj = {
        "client": PangolinfoClient(base_url=base_url),
        "token": token,
        "email": email,
        "password": password,
        "dry_run": dry_run,
    }


@cli.command("auth")
@click.option("--out", default=None, help="Write token to a file instead of stdout.")
@click.pass_context
def auth_cmd(ctx, out):
    client: PangolinfoClient = ctx.obj["client"]
    email = ctx.obj["email"]
    password = ctx.obj["password"]
    dry_run: bool = ctx.obj["dry_run"]

    if dry_run:
        payload = {
            "url": f"{client.base_url}/api/v1/auth",
            "json": {"email": "<email>", "password": "<password>"},
        }
        if out:
            write_json(out, payload)
        else:
            click.echo(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return

    if not email or not password:
        raise click.ClickException(
            "Auth requires email+password. Provide --email+--password or env PANGOLINFO_EMAIL+PANGOLINFO_PASSWORD."
        )

    token = client.auth(email=email, password=password)
    if out:
        write_text(out, token + "\n")
    else:
        click.echo(token)


@cli.command("product")
@click.option("--asin", default=None, help="ASIN code for amzProductDetail.")
@click.option("--url", default=None, help="Amazon product URL (optional; if provided, still sends site/content).")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--zipcode", default=None, help="Amazon zipcode for bizContext.zipcode (optional).")
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="product.json", show_default=True)
@click.option("--out-format", type=click.Choice(["json", "csv"], case_sensitive=False), default="json", show_default=True)
@click.pass_context
def product_cmd(ctx, asin, url, site, zipcode, format_, out, out_format):
    if not asin and not url:
        raise click.ClickException("product requires --asin or --url.")

    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = build_product_detail_request(
        asin=asin,
        url=url,
        site=site,
        zipcode=zipcode,
        format=format_,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=req.to_json(),
        timeout_s=90,
        dry_run=ctx.obj["dry_run"],
    )

    if out_format == "json":
        write_json(out, payload)
        return

    results = extract_results_list(payload)
    columns = [
        "asin",
        "title",
        "price",
        "star",
        "rating",
        "badge",
        "sales",
        "brand",
        "seller",
        "shipper",
        "inStock",
        "category_id",
        "category_name",
        "parentAsin",
        "image",
    ]
    write_csv(out, results, columns=columns)


@cli.command("keyword")
@click.option("--q", "keyword", required=True, help="Keyword for amzKeyword.")
@click.option("--url", default=None, help="Amazon URL (optional; if omitted, uses site+content per docs).")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--zipcode", default=None, help="Amazon zipcode for bizContext.zipcode (optional).")
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="keyword.json", show_default=True)
@click.option("--out-format", type=click.Choice(["json", "csv"], case_sensitive=False), default="json", show_default=True)
@click.pass_context
def keyword_cmd(ctx, keyword, url, site, zipcode, format_, out, out_format):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = build_keyword_request(
        keyword=keyword,
        url=url,
        site=site,
        zipcode=zipcode,
        format=format_,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=req.to_json(),
        timeout_s=90,
        dry_run=ctx.obj["dry_run"],
    )

    if out_format == "json":
        write_json(out, payload)
        return

    results = extract_results_list(payload)
    columns = [
        "asin",
        "title",
        "price",
        "star",
        "rating",
        "image",
        "sales",
        "rank",
        "sponsored",
        "spRank",
        "badge",
        "delivery",
    ]
    write_csv(out, results, columns=columns)


@cli.command("reviews")
@click.option("--asin", required=True, help="ASIN code for amzReviewV2.")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--page-count", type=int, default=1, show_default=True)
@click.option("--filter-by-star", default="all_stars", show_default=True)
@click.option("--sort-by", default="recent", show_default=True)
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--format-type", type=click.Choice(["all_formats", "current_format"], case_sensitive=False), default="all_formats", show_default=True)
@click.option("--media-type", type=click.Choice(["all_contents", "media_reviews_only"], case_sensitive=False), default="all_contents", show_default=True)
@click.option("--out", default="reviews.json", show_default=True)
@click.option("--out-format", type=click.Choice(["json", "csv"], case_sensitive=False), default="json", show_default=True)
@click.pass_context
def reviews_cmd(
    ctx,
    asin,
    site,
    page_count,
    filter_by_star,
    sort_by,
    format_,
    format_type,
    media_type,
    out,
    out_format,
):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    body = build_reviews_request(
        asin=asin,
        site=site,
        page_count=page_count,
        filter_by_star=filter_by_star,
        sort_by=sort_by,
        format=format_,
        format_type=format_type,
        media_type=media_type,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=body,
        timeout_s=180,
        dry_run=ctx.obj["dry_run"],
    )

    if out_format == "json":
        write_json(out, payload)
        return

    results = extract_results_list(payload)
    columns = [
        "date",
        "country",
        "star",
        "reviewLink",
        "author",
        "authorId",
        "title",
        "content",
        "purchased",
        "vineVoice",
        "helpful",
        "reviewId",
    ]
    write_csv(out, results, columns=columns)


@cli.command("category")
@click.option("--node-id", "category_node_id", required=True, help="Category Node ID for amzProductOfCategory.")
@click.option("--url", default=None, help="Amazon URL (optional; if omitted, uses site+content per docs).")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--zipcode", default=None, help="Amazon zipcode for bizContext.zipcode (optional).")
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="category.json", show_default=True)
@click.pass_context
def category_cmd(ctx, category_node_id, url, site, zipcode, format_, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = build_category_products_request(
        category_node_id=category_node_id,
        url=url,
        site=site,
        zipcode=zipcode,
        format=format_,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=req.to_json(),
        timeout_s=90,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@cli.command("seller")
@click.option("--seller-id", required=True, help="Seller ID for amzProductOfSeller.")
@click.option("--url", default=None, help="Amazon URL (optional; if omitted, uses site+content per docs).")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--zipcode", default=None, help="Amazon zipcode for bizContext.zipcode (optional).")
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="seller.json", show_default=True)
@click.option("--out-format", type=click.Choice(["json", "csv"], case_sensitive=False), default="json", show_default=True)
@click.pass_context
def seller_cmd(ctx, seller_id, url, site, zipcode, format_, out, out_format):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = build_seller_products_request(
        seller_id=seller_id,
        url=url,
        site=site,
        zipcode=zipcode,
        format=format_,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=req.to_json(),
        timeout_s=120,
        dry_run=ctx.obj["dry_run"],
    )

    if out_format == "json":
        write_json(out, payload)
        return

    results = extract_results_list(payload)
    columns = ["asin", "title", "price", "star", "rating", "image"]
    write_csv(out, results, columns=columns)


@cli.command("best-sellers")
@click.option("--keyword", "best_sellers_keyword", required=True, help="Best Sellers category keyword for amzBestSellers.")
@click.option("--url", default=None, help="Amazon URL (optional; if omitted, uses site+content per docs).")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--zipcode", default=None, help="Amazon zipcode for bizContext.zipcode (optional).")
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="best_sellers.json", show_default=True)
@click.pass_context
def best_sellers_cmd(ctx, best_sellers_keyword, url, site, zipcode, format_, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = build_best_sellers_request(
        best_sellers_keyword=best_sellers_keyword,
        url=url,
        site=site,
        zipcode=zipcode,
        format=format_,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=req.to_json(),
        timeout_s=120,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@cli.command("new-releases")
@click.option("--keyword", "new_releases_keyword", required=True, help="New Releases category keyword for amzNewReleases.")
@click.option("--url", default=None, help="Amazon URL (optional; if omitted, uses site+content per docs).")
@click.option("--site", default="amz_us", show_default=True)
@click.option("--zipcode", default=None, help="Amazon zipcode for bizContext.zipcode (optional).")
@click.option("--format", "format_", type=click.Choice(["json"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="new_releases.json", show_default=True)
@click.pass_context
def new_releases_cmd(ctx, new_releases_keyword, url, site, zipcode, format_, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = build_new_releases_request(
        new_releases_keyword=new_releases_keyword,
        url=url,
        site=site,
        zipcode=zipcode,
        format=format_,
    )
    payload = client.post(
        path="/api/v1/scrape",
        token=token,
        json_body=req.to_json(),
        timeout_s=120,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@cli.command("universal")
@click.option("--url", "urls", multiple=True, required=True, help="Target URL. Repeat to pass multiple URLs.")
@click.option("--format", "format_", type=click.Choice(["rawHtml", "markdown"], case_sensitive=False), default="markdown", show_default=True)
@click.option("--timeout-ms", type=int, default=40000, show_default=True)
@click.option("--mode", type=click.Choice(["json", "content"], case_sensitive=False), default="json", show_default=True)
@click.option("--out", default="universal.json", show_default=True)
@click.pass_context
def universal_cmd(ctx, urls, format_, timeout_ms, mode, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = UniversalScrapeBatchRequest(urls=list(urls), format=format_, timeout_ms=timeout_ms)
    payload = client.post(
        path="/api/v1/scrape/batch",
        token=token,
        json_body=req.to_json(),
        timeout_s=max(10, int(timeout_ms / 1000) + 10),
        dry_run=ctx.obj["dry_run"],
    )

    if mode == "json":
        write_json(out, payload)
        return

    field = "rawHtml" if format_.lower() == "rawhtml" else "markdown"
    content = try_extract_universal_content(payload, field=field)
    if content is None:
        raise click.ClickException(f"Response does not contain field '{field}' to extract. Use --mode json to inspect full response.")
    write_text(out, content + "\n")


@cli.group("niche")
def niche_group():
    pass


@niche_group.command("category-children")
@click.option("--parent-path", required=True, help="parentBrowseNodeIdPath (e.g. 2619526011 or 2619526011/18116197011)")
@click.option("--page", type=int, default=1, show_default=True)
@click.option("--size", type=int, default=10, show_default=True)
@click.option("--out", default="category_children.json", show_default=True)
@click.pass_context
def niche_category_children(ctx, parent_path, page, size, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = CategoryChildrenRequest(parent_browse_node_id_path=parent_path, page=page, size=size)
    payload = client.post(
        path="/api/v1/amzscope/categories/children",
        token=token,
        json_body=req.to_json(),
        timeout_s=60,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@niche_group.command("category-search")
@click.option("--keyword", required=True)
@click.option("--page", type=int, default=1, show_default=True)
@click.option("--size", type=int, default=10, show_default=True)
@click.option("--out", default="category_search.json", show_default=True)
@click.pass_context
def niche_category_search(ctx, keyword, page, size, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = CategorySearchRequest(keyword=keyword, page=page, size=size)
    payload = client.post(
        path="/api/v1/amzscope/categories/search",
        token=token,
        json_body=req.to_json(),
        timeout_s=60,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@niche_group.command("category-paths")
@click.option("--category-id", "category_ids", multiple=True, required=True, help="Repeat to pass multiple IDs.")
@click.option("--out", default="category_paths.json", show_default=True)
@click.pass_context
def niche_category_paths(ctx, category_ids, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = CategoryPathsRequest(category_ids=list(category_ids))
    payload = client.post(
        path="/api/v1/amzscope/categories/paths",
        token=token,
        json_body=req.to_json(),
        timeout_s=60,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@niche_group.command("category-filter")
@click.option("--marketplace-id", default="US", show_default=True, type=click.Choice(["US"], case_sensitive=False))
@click.option("--time-range", default="l7d", show_default=True, type=click.Choice(["l7d", "l30d", "l90d", "l12m"], case_sensitive=False))
@click.option("--sample-scope", default="all_asin", show_default=True, type=click.Choice(["all_asin", "new_successful", "top_grossing"], case_sensitive=False))
@click.option("--category-id", default=None)
@click.option("--page", type=int, default=1, show_default=True)
@click.option("--size", type=int, default=10, show_default=True)
@click.option("--sort-field", default=None)
@click.option("--sort-order", default=None, type=click.Choice(["asc", "desc"], case_sensitive=False))
@click.option("--out", default="category_filter.json", show_default=True)
@click.pass_context
def niche_category_filter(
    ctx,
    marketplace_id,
    time_range,
    sample_scope,
    category_id,
    page,
    size,
    sort_field,
    sort_order,
    out,
):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = CategoryFilterRequest(
        marketplace_id=marketplace_id,
        time_range=time_range,
        sample_scope=sample_scope,
        category_id=category_id,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
    )
    payload = client.post(
        path="/api/v1/amzscope/categories/filter",
        token=token,
        json_body=req.to_json(),
        timeout_s=90,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


@niche_group.command("filter")
@click.option("--marketplace-id", default="US", show_default=True, type=click.Choice(["US"], case_sensitive=False))
@click.option("--niche-id", default=None)
@click.option("--niche-title", default=None)
@click.option("--page", type=int, default=1, show_default=True)
@click.option("--size", type=int, default=10, show_default=True)
@click.option("--sort-field", default=None)
@click.option("--sort-order", default=None, type=click.Choice(["asc", "desc"], case_sensitive=False))
@click.option("--out", default="niche_filter.json", show_default=True)
@click.pass_context
def niche_filter(ctx, marketplace_id, niche_id, niche_title, page, size, sort_field, sort_order, out):
    client: PangolinfoClient = ctx.obj["client"]
    token = _resolve_token(
        client,
        token=ctx.obj["token"],
        email=ctx.obj["email"],
        password=ctx.obj["password"],
        dry_run=ctx.obj["dry_run"],
    )
    req = NicheFilterRequest(
        marketplace_id=marketplace_id,
        niche_id=niche_id,
        niche_title=niche_title,
        page=page,
        size=size,
        sort_field=sort_field,
        sort_order=sort_order,
    )
    payload = client.post(
        path="/api/v1/amzscope/niches/filter",
        token=token,
        json_body=req.to_json(),
        timeout_s=120,
        dry_run=ctx.obj["dry_run"],
    )
    write_json(out, payload)


def main():
    try:
        cli()
    except PangolinfoError as e:
        raise click.ClickException(str(e)) from e


if __name__ == "__main__":
    main()
