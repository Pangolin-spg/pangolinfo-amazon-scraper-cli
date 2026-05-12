# Pangolinfo 亚马逊爬虫（Real-time JSON/Markdown for AI Agents）

<p>
  <img src="images/banner_cn.png" alt="Pangolinfo Amazon Scraper" width="100%">
</p>

如果你需要 **高效、低成本、快速** 地采集 Amazon 数据（商品、关键词搜索、评论、榜单、类目/利基指标），这个项目提供一个“可复制命令、可审计请求、可落盘输出”的开源 CLI：直接调用 Pangolinfo 的官方接口，输出 **高度定制化、实时化、AI 友好的 JSON / Markdown**，用于：

- Amazon 竞品监控、关键词排名追踪、评论分析、类目研究
- Agent（Tool Calling / MCP / OpenClaw）所需的实时结构化数据输入
- RAG / 数据管道（JSON 便于结构化，Markdown 便于切块检索）

核心观点：Agent 是否靠谱，首先取决于输入是否靠谱；而“靠谱输入”通常意味着 **实时、可验证、结构化**。

## 官方链接与免费试用

- 官网：https://www.pangolinfo.com/?referrer=github_amz
- 控制台｜获取 API Key：https://tool.pangolinfo.com/?referrer=github_amz
- 文档：https://docs.pangolinfo.com/?referrer=github_amz
- Scrape API：https://www.pangolinfo.com/zh/scraping-api/?referrer=github_amz
- Amazon Niche Data API：https://www.pangolinfo.com/zh/cn-amazon-niche-data-api/?referrer=github_amz
- AI SERP API：https://www.pangolinfo.com/zh/google-ai-overview-api/?referrer=github_amz
- Amazon Scraper Skill：https://www.pangolinfo.com/zh/pangolinfo-amazon-scraper-skill/?referrer=github_amz
- AI SERP Skill：https://www.pangolinfo.com/zh/pangolinfo-ai-serp-api-skill/?referrer=github_amz

行动号召：去控制台免费获取 API Key 做测试，新注册账号会赠送免费测试积分。https://tool.pangolinfo.com/?referrer=github_amz

## 目录

- [开源 Pangolinfo 亚马逊爬虫 CLI](#开源-pangolinfo-亚马逊爬虫-cli)
  - [前提条件](#前提条件)
  - [快速设置](#快速设置)
  - [如何抓取亚马逊实时数据](#如何抓取亚马逊实时数据)
  - [输出](#输出)
- [爬取亚马逊数据的挑战](#爬取亚马逊数据的挑战)
- [解决方案：Pangolinfo 实时 Scrape API + Skill + Niche Data API](#解决方案pangolinfo-实时-scrape-api--skill--niche-data-api)
  - [Amazon Scrape Skill（Agent 直接用）](#amazon-scrape-skillagent-直接用)
  - [Amazon Niche Data API（选品类目垄断度趋势）](#amazon-niche-data-api选品类目垄断度趋势)
- [Pangolinfo API 实践](#pangolinfo-api-实践)
  - [认证（Bearer Token）](#认证bearer-token)
  - [Amazon Scrape API：通用参数](#amazon-scrape-api通用参数)
  - [Amazon Review API：通用参数](#amazon-review-api通用参数)
  - [General Scrape API：通用参数](#general-scrape-api通用参数)
  - [Amazon Niche Data API：通用参数](#amazon-niche-data-api通用参数)
  - [商品详情（amzProductDetail）](#商品详情amzproductdetail)
  - [关键词搜索（amzKeyword）](#关键词搜索amzkeyword)
  - [评论（amzReviewV2）](#评论amzreviewv2)
  - [按卖家抓取商品（amzProductOfSeller）](#按卖家抓取商品amzproductofseller)
  - [按类目抓取商品（amzProductOfCategory）](#按类目抓取商品amzproductofcategory)
  - [畅销榜（amzBestSellers）](#畅销榜amzbestsellers)
  - [新品榜（amzNewReleases）](#新品榜amznewreleases)
  - [类目树（Category Tree API）](#类目树category-tree-api)
  - [类目搜索（Search Categories API）](#类目搜索search-categories-api)
  - [类目路径（Batch Category Paths API）](#类目路径batch-category-paths-api)
  - [类目过滤（Category Filter API）](#类目过滤category-filter-api)
  - [利基过滤（Niche Filter API）](#利基过滤niche-filter-api)
- [Dry-run（不确定时用它，不猜）](#dry-run不确定时用它不猜)
- [给 AI Agent 的数据建议（JSON / Markdown）](#给-ai-agent-的数据建议json--markdown)
- [可选截图素材（用于 SEO 与转化）](#可选截图素材用于-seo-与转化)

## 开源 Pangolinfo 亚马逊爬虫 CLI

这个 CLI 的目标不是“模拟浏览器爬网页”，而是把 Pangolinfo 的实时数据能力封装成更适合开发者与 Agent 的交互方式：参数可控、输出可控、且完全对齐官方文档。

### 前提条件

- Python 3.9 或更高版本
- 有 Pangolinfo 的长期 Token（或用 email+password 通过 Auth API 换取）

### 快速设置

1) 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

2) 配置 Token（推荐：环境变量）

```bash
export PANGOLINFO_TOKEN="YOUR_TOKEN"
```

3) 查看命令帮助

```bash
python3 main.py --help
```

### 如何抓取亚马逊实时数据

这个仓库支持两类输出：

- **JSON**：适合 Agent 做结构化推理与可验证引用
- **Markdown**：适合 RAG 切块、检索、摘要与引用（来自 General Scrape API）

典型命令（更多见下方“Pangolinfo API 实践”）：

```bash
python3 main.py product --asin B0DYTF8L2W --site amz_us --zipcode 10041 --out product.json
python3 main.py keyword --q "coffee maker" --site amz_us --out keyword.json
python3 main.py reviews --asin B076CLQDR4 --page-count 2 --out reviews.json
python3 main.py universal --url "https://www.amazon.com/dp/B0B41YH9B6" --format markdown --mode content --out page.md
```

### 输出

默认输出文件会写到当前目录（`--out` 可自定义）。

- JSON：完整保留 Pangolinfo 响应，便于审计与回放
- CSV：仅导出常用字段（不丢原始 JSON；你仍可输出 JSON 作为来源记录）
- Markdown：可直接喂给 Agent/RAG（`universal --mode content`）

CSV 列（本仓库导出列基于官方字段名）：

- `keyword --out-format csv`：`asin,title,price,star,rating,image,sales,rank,sponsored,spRank,badge,delivery`
- `reviews --out-format csv`：`date,country,star,reviewLink,author,authorId,title,content,purchased,vineVoice,helpful,reviewId`
- `product --out-format csv`：`asin,title,price,star,rating,badge,sales,brand,seller,shipper,inStock,category_id,category_name,parentAsin,image`

## 爬取亚马逊数据的挑战

“能打开网页”不等于“能稳定拿到数据”。真实业务里常见的难点包括：

1) **反爬与挑战页面**：CAPTCHA、行为检测、频繁的人机校验会让自建爬虫不稳定。  
2) **页面结构频繁变动**：DOM 变动意味着解析逻辑需要持续维护。  
3) **Agent 的数据要求更苛刻**：Agent 不仅要“看见内容”，还要 **可验证、可复用、可抽取的结构化结果**。  
4) **实时性**：排名、广告位、评论、类目指标都是强时效信号；过期数据会让 Agent 产生“看似合理、实际错误”的推理。

<p>
  <img src="images/amazon_serp_page.png" alt="Amazon SERP (example)" width="100%">
</p>

<p>
  <img src="images/amazon_blocked.png" alt="Amazon blocked / CAPTCHA (example)" width="100%">
</p>

## 解决方案：Pangolinfo 实时 Scrape API + Skill + Niche Data API

Pangolinfo 把“反爬 + 解析模板 + 实时输出”封装成 API/Skill，开发侧的重点回到：选择 parser、定义你要的字段、把结果喂给 Agent。

### Amazon Scrape Skill（Agent 直接用）

如果你已经在用 Agent（OpenClaw / MCP / Tool Calling），可以优先考虑直接安装官方 Skill：

- Skills 总览：https://docs.pangolinfo.com/en-help-center/skills?referrer=github_amz
- Pangolinfo Amazon Scraper Skill：https://www.pangolinfo.com/amazon-scraper-skill/?referrer=github_amz
- Skill Package Download（来自官方 Skills 页）：https://wry-manatee-359.convex.site/api/v1/download?slug=pangolinfo-amazon-scraper

Clawhub 一键安装（来自官方 Skills 页）：

```bash
openclaw skills install pangolinfo-amazon-scraper
```

这个仓库适合以下场景：

- 你需要“可审计”的 API 请求/响应落盘（debug、对账、回放）
- 你要把 Pangolinfo API 接入自有服务或自定义 Agent 工具层（而不是只装 Skill）

### Amazon Niche Data API（选品类目垄断度趋势）

Niche Data 用于类目/利基维度的结构化指标，适合做选品与“市场情报”的 Agent 推理输入。

- Niche Data Skill（官方 Skills 页）：https://docs.pangolinfo.com/en-help-center/skills?referrer=github_amz
- Skill Package Download（来自官方 Skills 页）：https://wry-manatee-359.convex.site/api/v1/download?slug=pangolinfo-amazon-niche

Clawhub 一键安装（来自官方 Skills 页）：

```bash
openclaw skills install pangolinfo-amazon-niche
```

## Pangolinfo API 实践

本节按“参考项目”的细致程度，把每个接口/用例拆成：关键参数、命令示例、以及（必要时）cURL 示例。

### 认证（Bearer Token）

Auth 文档：https://docs.pangolinfo.com/en-api-reference/authApi/authApi?referrer=github_amz

请求：

- URL：`POST https://scrapeapi.pangolinfo.com/api/v1/auth`
- Body：`{"email":"...","password":"..."}`

CLI（从环境变量读账号密码，输出 token）：

```bash
export PANGOLINFO_EMAIL="you@example.com"
export PANGOLINFO_PASSWORD="your-password"
python3 main.py auth
```

### Amazon Scrape API：通用参数

文档：https://docs.pangolinfo.com/en-api-reference/amazonApi/amazonScrapeAPI?referrer=github_amz

请求：

- URL：`POST https://scrapeapi.pangolinfo.com/api/v1/scrape`
- Headers：`Authorization: Bearer <token>`、`Content-Type: application/json`

关键参数（按官方文档描述）：

| 参数 | 必填 | 类型 | 说明 |
|---|---:|---|---|
| url | 是（或用 site+content） | string | 目标 URL；不传时需要 `site` 与 `content` |
| parserName | 是 | string | `amzProductDetail` / `amzKeyword` / `amzProductOfCategory` / `amzProductOfSeller` / `amzBestSellers` / `amzNewReleases` |
| site | 是（url 传了也可传） | string | 站点信息（示例：`amz_us`） |
| content | 是（或 url） | string | 随 parserName 而变：ASIN / keyword / category node id / seller id 等 |
| format | 是 | string | `json` |
| bizContext | 是 | object | 业务上下文（例如 `zipcode`） |

### Amazon Review API：通用参数

文档：https://docs.pangolinfo.com/en-api-reference/amazonReviewAPI/submit?referrer=github_amz

请求同样走 `POST /api/v1/scrape`，但参数结构不同：

| 参数 | 必填 | 类型 | 说明 |
|---|---:|---|---|
| url | 是 | string | 默认 `https://www.amazon.com`（见官方示例） |
| site | 是 | string | `amz_us` / `amz_de` / `amz_uk` / `amz_jp` / `amz_fr` / `amz_it` / `amz_es` / `amz_ca` |
| format | 是 | string | `json` |
| formatType | 是 | string | `all_formats` / `current_format` |
| mediaType | 是 | string | `all_contents` / `media_reviews_only` |
| parserName | 是 | string | `amzReviewV2` |
| bizContext | 是 | object | `bizKey/pageCount/asin/filterByStar/sortBy` |

### General Scrape API：通用参数

文档：https://docs.pangolinfo.com/en-api-reference/universalApi/universalApi?referrer=github_amz

- URL：`POST https://scrapeapi.pangolinfo.com/api/v1/scrape/batch`
- 参数：`urls[]`、`format (rawHtml|markdown)`、可选 `timeout`（毫秒）

### Amazon Niche Data API：通用参数

本仓库实现的 Niche Data 端点全部来自官方 Playground：

- Category Tree API：https://docs.pangolinfo.com/en-api-reference/browseCategoryTreeAPI/submit?referrer=github_amz
- Search Categories API：https://docs.pangolinfo.com/en-api-reference/searchCategoriesAPI/submit?referrer=github_amz
- Batch Category Paths API：https://docs.pangolinfo.com/en-api-reference/batchCategoryPathsAPI/submit?referrer=github_amz
- Category Filter API：https://docs.pangolinfo.com/en-api-reference/categoryFilterAPI/submit?referrer=github_amz
- Niche Filter API：https://docs.pangolinfo.com/en-api-reference/nicheFilterAPI/submit?referrer=github_amz

---

### 商品详情（amzProductDetail）

CLI：

```bash
python3 main.py product --asin B0DYTF8L2W --site amz_us --zipcode 10041 --out product.json
```

cURL（基于官方示例结构）：

```bash
curl -X POST "https://scrapeapi.pangolinfo.com/api/v1/scrape" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.amazon.com/dp/B0DYTF8L2W",
    "parserName": "amzProductDetail",
    "site": "amz_us",
    "content": "",
    "format": "json",
    "bizContext": {
      "zipcode": "10041"
    }
  }'
```

### 关键词搜索（amzKeyword）

CLI：

```bash
python3 main.py keyword --q "coffee maker" --site amz_us --out keyword.json
python3 main.py keyword --q "coffee maker" --out keyword.csv --out-format csv
```

<p>
  <img src="images/output_keyword_json_preview.png" alt="Keyword results JSON (preview)" width="100%">
</p>

<details>
  <summary>点击展开完整 Keyword JSON 示例</summary>
  <p>
    <img src="images/output_keyword_json.png" alt="Keyword results JSON (full)" width="100%">
  </p>
</details>

### 评论（amzReviewV2）

CLI：

```bash
python3 main.py reviews --asin B076CLQDR4 --site amz_us --page-count 1 --sort-by recent --out reviews.json
python3 main.py reviews --asin B076CLQDR4 --out reviews.csv --out-format csv
```

cURL（来自官方 Playground 示例）：

```bash
curl --request POST \
  --url https://scrapeapi.pangolinfo.com/api/v1/scrape \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "url": "https://www.amazon.com",
    "site": "amz_us",
    "format": "json",
    "formatType": "all_formats",
    "mediaType": "all_contents",
    "parserName": "amzReviewV2",
    "bizContext": {
      "bizKey": "review",
      "pageCount": 1,
      "asin": "B076CLQDR4",
      "filterByStar": "all_stars",
      "sortBy": "recent"
    }
  }'
```

### 按卖家抓取商品（amzProductOfSeller）

说明：`content` 为 Seller ID（来自 Amazon Scrape API 文档的 parser 说明）。

CLI：

```bash
python3 main.py seller --seller-id "<seller_id>" --site amz_us --out seller.json
python3 main.py seller --seller-id "<seller_id>" --out seller.csv --out-format csv
```

### 按类目抓取商品（amzProductOfCategory）

CLI：

```bash
python3 main.py category --node-id "<category_node_id>" --site amz_us --out category.json
```

### 畅销榜（amzBestSellers）

CLI：

```bash
python3 main.py best-sellers --keyword "<best_sellers_category_keyword>" --site amz_us --out best_sellers.json
```

### 新品榜（amzNewReleases）

CLI：

```bash
python3 main.py new-releases --keyword "<new_releases_category_keyword>" --site amz_us --out new_releases.json
```

### 类目树（Category Tree API）

CLI（对应官方 `POST /api/v1/amzscope/categories/children`）：

```bash
python3 main.py niche category-children --parent-path 2619526011 --page 1 --size 10 --out children.json
```

### 类目搜索（Search Categories API）

CLI（对应官方 `POST /api/v1/amzscope/categories/search`）：

```bash
python3 main.py niche category-search --keyword headphones --page 1 --size 10 --out category_search.json
```

### 类目路径（Batch Category Paths API）

CLI（对应官方 `POST /api/v1/amzscope/categories/paths`）：

```bash
python3 main.py niche category-paths --category-id 2619526011 --category-id 172282 --out category_paths.json
```

### 类目过滤（Category Filter API）

文档示例请求体包含：

| 参数 | 必填 | 说明 |
|---|---:|---|
| marketplaceId | 是 | 当前文档可选项包含 `US` |
| timeRange | 是 | `l7d/l30d/l90d/l12m` |
| sampleScope | 是 | `all_asin/new_successful/top_grossing` |
| categoryId | 否 | 指定则返回该类目记录 |
| page/size | 是 | 分页；size 最大 10 |
| sortField/sortOrder | 否 | sortField 支持任意返回字段名 |

CLI：

```bash
python3 main.py niche category-filter --marketplace-id US --time-range l7d --sample-scope all_asin --category-id 979832011 --page 1 --size 10 --out category_filter.json
```

### 利基过滤（Niche Filter API）

CLI：

```bash
python3 main.py niche filter --marketplace-id US --niche-title "iphone 16 wallet case" --page 1 --size 10 --out niche_filter.json
```

## Dry-run（不确定时用它，不猜）

所有命令都支持 `--dry-run`：只打印请求 JSON，不发请求。

```bash
python3 main.py --dry-run keyword --q "coffee maker" --site amz_us
python3 main.py --dry-run niche category-filter --marketplace-id US --time-range l7d --sample-scope all_asin --category-id 979832011
```

## 给 AI Agent 的数据建议（JSON / Markdown）

这部分是“如何用数据喂 Agent”的工程建议，不是接口字段规范：

- 优先用 JSON 做 Agent 的主输入（可验证字段、可控 schema、可做差异对比）
- Markdown 适合做 RAG（切块、检索、引用），建议只用 `universal --mode content` 输出的干净文本，而不是 HTML
- 做“高度定制化”时，建议先用 `--dry-run` 固化请求体，再基于你要的字段做裁剪与标准化输出

## 可选截图素材（用于 SEO 与转化）

如果你希望 README 像参考项目一样“图文并茂”（更利于 GitHub SEO 与转化、也更利于用户快速理解输出），建议提供以下截图，并按文件名放入本仓库的 `images/` 目录：

- `images/banner_cn.png`：README 顶部横幅（品牌 + 价值主张）
- `images/output_keyword_json.png`：关键词搜索 API 返回 JSON 的截图（展示 `results` 中若干条商品字段）
- `images/output_keyword_json_preview.png`：上图的“预览裁剪版”（只截一屏，用于 README 默认展示）
- `images/output_reviews_json.png`：评论 JSON 输出的截图（展示 `results` 中一条评论的字段）
- `images/niche_category_filter.png`：Category Filter API 输出示例截图（展示类目指标字段）
- `images/skills_install.png`：Skills 页面中 Amazon Scraper Skill 与 Amazon Niche Data 的截图（包含安装命令）

可选（用来解释“为什么不要自己爬前端页面”）：

- `images/amazon_serp_page.png`：Amazon 搜索结果页截图（只做“场景示意”）
- `images/amazon_blocked.png`：Amazon 被拦截/CAPTCHA/挑战页截图（用来解释反爬挑战）

截图建议：

- 宽度 ≥ 1200px，字段清晰可读
- 不要包含任何 token/password
