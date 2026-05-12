# Pangolinfo 亚马逊爬虫（Real-time JSON/Markdown for AI Agents）

<p>
  <img src="images/banner_cn.png" alt="Pangolinfo Amazon Scraper" width="100%">
</p>

如果你需要 **高效、低成本、快速** 地采集 Amazon 数据（商品、关键词搜索、评论、榜单、类目/利基指标），这个项目提供一个“可复制命令、可审计请求、可落盘输出”的开源 CLI：直接调用 Pangolinfo 的官方接口，输出 **高度定制化、实时化、AI 友好的 JSON / Markdown**，用于：

- Amazon 竞品监控、关键词排名追踪、评论分析、类目研究
- Agent（Tool Calling / MCP / OpenClaw）所需的实时结构化数据输入
- RAG / 数据管道（JSON 便于结构化，Markdown 便于切块检索）

你将解决：

- 反爬与 DOM 变更带来的高维护成本：用 API/Skill 获取稳定结构化输出
- 数据不够实时导致的误判：用实时数据驱动选品、竞品监控与 Agent 决策
- 数据不够“AI 友好”导致的不可用：优先 JSON/Markdown 作为 AI 输入格式

核心观点：Agent 是否靠谱，首先取决于输入是否靠谱；而“靠谱输入”通常意味着 **实时、可验证、结构化**。

## 官网入口与免费试用

<p>
  <a href="https://www.pangolinfo.com/?referrer=github_amz" target="_blank" rel="noopener noreferrer">官网</a>｜
  <a href="https://tool.pangolinfo.com/?referrer=github_amz" target="_blank" rel="noopener noreferrer">控制台｜获取 API Key</a>｜
  <a href="https://docs.pangolinfo.com/?referrer=github_amz" target="_blank" rel="noopener noreferrer">文档</a>｜
  <a href="https://www.pangolinfo.com/zh/scraping-api/?referrer=github_amz" target="_blank" rel="noopener noreferrer">Scrape API</a>｜
  <a href="https://www.pangolinfo.com/zh/cn-amazon-niche-data-api/?referrer=github_amz" target="_blank" rel="noopener noreferrer">Amazon Niche Data API</a>｜
  <a href="https://www.pangolinfo.com/zh/google-ai-overview-api/?referrer=github_amz" target="_blank" rel="noopener noreferrer">AI SERP API</a>｜
  <a href="https://www.pangolinfo.com/zh/pangolinfo-amazon-scraper-skill/?referrer=github_amz" target="_blank" rel="noopener noreferrer">Amazon Scraper Skill</a>｜
  <a href="https://www.pangolinfo.com/zh/pangolinfo-ai-serp-api-skill/?referrer=github_amz" target="_blank" rel="noopener noreferrer">AI SERP Skill</a>
</p>

免费试用：前往<a href="https://tool.pangolinfo.com/?referrer=github_amz" target="_blank" rel="noopener noreferrer">控制台</a>注册并生成 API Key，新用户可获得免费测试积分，用于验证接口效果与数据准确性。

## 🔥 复制即用（3 个最常用命令）

```bash
python3 main.py product --asin B0DYTF8L2W --site amz_us --zipcode 10041 --out product.json
python3 main.py keyword --q "coffee maker" --site amz_us --out keyword.json
python3 main.py reviews --asin B076CLQDR4 --site amz_us --page-count 1 --sort-by recent --out reviews.json
```

## 目录

- <a href="#开源-pangolinfo-亚马逊爬虫-cli" target="_blank" rel="noopener noreferrer">开源 Pangolinfo 亚马逊爬虫 CLI</a>
  - <a href="#前提条件" target="_blank" rel="noopener noreferrer">前提条件</a>
  - <a href="#快速设置" target="_blank" rel="noopener noreferrer">快速设置</a>
  - <a href="#如何抓取亚马逊实时数据" target="_blank" rel="noopener noreferrer">如何抓取亚马逊实时数据</a>
  - <a href="#输出" target="_blank" rel="noopener noreferrer">输出</a>
- <a href="#爬取亚马逊数据的挑战" target="_blank" rel="noopener noreferrer">爬取亚马逊数据的挑战</a>
- <a href="#解决方案pangolinfo-实时-scrape-api--skill--niche-data-api" target="_blank" rel="noopener noreferrer">解决方案：Pangolinfo 实时 Scrape API + Skill + Niche Data API</a>
  - <a href="#amazon-scrape-skillagent-直接用" target="_blank" rel="noopener noreferrer">Amazon Scrape Skill（Agent 直接用）</a>
  - <a href="#amazon-niche-data-api选品类目垄断度趋势" target="_blank" rel="noopener noreferrer">Amazon Niche Data API（选品类目垄断度趋势）</a>
- <a href="#pangolinfo-api-实践" target="_blank" rel="noopener noreferrer">Pangolinfo API 实践</a>
  - <a href="#认证bearer-token" target="_blank" rel="noopener noreferrer">认证（Bearer Token）</a>
  - <a href="#amazon-scrape-api通用参数" target="_blank" rel="noopener noreferrer">Amazon Scrape API：通用参数</a>
  - <a href="#amazon-review-api通用参数" target="_blank" rel="noopener noreferrer">Amazon Review API：通用参数</a>
  - <a href="#general-scrape-api通用参数" target="_blank" rel="noopener noreferrer">General Scrape API：通用参数</a>
  - <a href="#amazon-niche-data-api通用参数" target="_blank" rel="noopener noreferrer">Amazon Niche Data API：通用参数</a>
  - <a href="#商品详情amzproductdetail" target="_blank" rel="noopener noreferrer">商品详情（amzProductDetail）</a>
  - <a href="#关键词搜索amzkeyword" target="_blank" rel="noopener noreferrer">关键词搜索（amzKeyword）</a>
  - <a href="#评论amzreviewv2" target="_blank" rel="noopener noreferrer">评论（amzReviewV2）</a>
  - <a href="#按卖家抓取商品amzproductofseller" target="_blank" rel="noopener noreferrer">按卖家抓取商品（amzProductOfSeller）</a>
  - <a href="#按类目抓取商品amzproductofcategory" target="_blank" rel="noopener noreferrer">按类目抓取商品（amzProductOfCategory）</a>
  - <a href="#畅销榜amzbestsellers" target="_blank" rel="noopener noreferrer">畅销榜（amzBestSellers）</a>
  - <a href="#新品榜amznewreleases" target="_blank" rel="noopener noreferrer">新品榜（amzNewReleases）</a>
  - <a href="#类目树category-tree-api" target="_blank" rel="noopener noreferrer">类目树（Category Tree API）</a>
  - <a href="#类目搜索search-categories-api" target="_blank" rel="noopener noreferrer">类目搜索（Search Categories API）</a>
  - <a href="#类目路径batch-category-paths-api" target="_blank" rel="noopener noreferrer">类目路径（Batch Category Paths API）</a>
  - <a href="#类目过滤category-filter-api" target="_blank" rel="noopener noreferrer">类目过滤（Category Filter API）</a>
  - <a href="#利基过滤niche-filter-api" target="_blank" rel="noopener noreferrer">利基过滤（Niche Filter API）</a>
- <a href="#dry-run不确定时用它不猜" target="_blank" rel="noopener noreferrer">Dry-run（不确定时用它，不猜）</a>
- <a href="#给-ai-agent-的数据建议json--markdown" target="_blank" rel="noopener noreferrer">给 AI Agent 的数据建议（JSON / Markdown）</a>
- <a href="#-立即开始" target="_blank" rel="noopener noreferrer">🎉 立即开始</a>

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

- <a href="https://docs.pangolinfo.com/en-help-center/skills?referrer=github_amz" target="_blank" rel="noopener noreferrer">Skills 总览</a>
- <a href="https://www.pangolinfo.com/amazon-scraper-skill/?referrer=github_amz" target="_blank" rel="noopener noreferrer">Pangolinfo Amazon Scraper Skill</a>
- <a href="https://wry-manatee-359.convex.site/api/v1/download?slug=pangolinfo-amazon-scraper" target="_blank" rel="noopener noreferrer">Skill Package Download（来自官方 Skills 页）</a>

Clawhub 一键安装（来自官方 Skills 页）：

```bash
openclaw skills install pangolinfo-amazon-scraper
```

这个仓库适合以下场景：

- 你需要“可审计”的 API 请求/响应落盘（debug、对账、回放）
- 你要把 Pangolinfo API 接入自有服务或自定义 Agent 工具层（而不是只装 Skill）

### Amazon Niche Data API（选品类目垄断度趋势）

Niche Data 用于类目/利基维度的结构化指标，适合做选品与“市场情报”的 Agent 推理输入。

- <a href="https://docs.pangolinfo.com/en-help-center/skills?referrer=github_amz" target="_blank" rel="noopener noreferrer">Niche Data Skill（官方 Skills 页）</a>
- <a href="https://wry-manatee-359.convex.site/api/v1/download?slug=pangolinfo-amazon-niche" target="_blank" rel="noopener noreferrer">Skill Package Download（来自官方 Skills 页）</a>

Clawhub 一键安装（来自官方 Skills 页）：

```bash
openclaw skills install pangolinfo-amazon-niche
```

## Pangolinfo API 实践

本节按“参考项目”的细致程度，把每个接口/用例拆成：关键参数、命令示例、以及（必要时）cURL 示例。

### 认证（Bearer Token）

Auth 文档：<a href="https://docs.pangolinfo.com/en-api-reference/authApi/authApi?referrer=github_amz" target="_blank" rel="noopener noreferrer">https://docs.pangolinfo.com/en-api-reference/authApi/authApi</a>

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

文档：<a href="https://docs.pangolinfo.com/en-api-reference/amazonApi/amazonScrapeAPI?referrer=github_amz" target="_blank" rel="noopener noreferrer">https://docs.pangolinfo.com/en-api-reference/amazonApi/amazonScrapeAPI</a>

请求：

- URL：`POST https://scrapeapi.pangolinfo.com/api/v1/scrape`
- Headers：`Authorization: Bearer <token>`、`Content-Type: application/json`

接口说明：

Amazon Scrape API 可动态兼容 Amazon 等电商页面结构变化，通过解析模板（`parserName`）自动提取结构化字段（标题、价格、库存、评分、评论等）。你只需要提供 URL 或 `site + content`，即可获得适合程序与 AI Agent 使用的实时 JSON 输出。

关键参数（按官方文档描述）：

| 参数 | 必填 | 类型 | 说明 |
|---|---:|---|---|
| url | 是（或用 site+content） | string | 目标 URL；不传时需要 `site` 与 `content` |
| parserName | 是 | string | `amzProductDetail` / `amzKeyword` / `amzProductOfCategory` / `amzProductOfSeller` / `amzBestSellers` / `amzNewReleases` |
| site | 是（url 传了也可传） | string | 站点信息（示例：`amz_us`） |
| content | 是（或 url） | string | 随 parserName 而变：ASIN / keyword / category node id / seller id 等 |
| format | 是 | string | `json` |
| bizContext | 是 | object | 业务上下文（例如 `zipcode`） |

`content` 与 `parserName` 的对应关系：

| parserName | content 应填什么 |
|---|---|
| amzProductDetail | ASIN |
| amzKeyword | 关键词（keyword） |
| amzProductOfCategory | 类目 Node ID |
| amzProductOfSeller | 卖家/店铺 ID（Seller ID） |
| amzBestSellers | 热卖榜类目关键词 |
| amzNewReleases | 新品榜类目关键词 |

返回结构（核心路径）：

- `code` / `message` / `data`
- 主要结果通常在：`data.json[0].data.results`

<details>
  <summary>点击展开：Amazon Scrape API 字段说明（按解析器）</summary>

#### amzProductDetail（商品详情）

| 字段 | 说明 |
|---|---|
| asin | ASIN 码 |
| title | 商品标题 |
| image | 主图链接 |
| price | 商品价格 |
| strikethroughPrice | 划线价格 |
| star | 商品评分 |
| rating | 评分数 |
| badge | 徽章 |
| acBadge | 是否 AC 标识 |
| sales | 商品销量 |
| images | 图片集 |
| seller | 卖家 |
| shipper | 发货方 |
| inStock | 库存 |
| merchant_id | 卖家 ID |
| color | 颜色 |
| size | 尺寸 |
| brand | 品牌 |
| has_cart | 是否有购物车 |
| followSeller | 跟卖信息 |
| features | 五点描述 |
| coupon | 优惠券 |
| ratingDistribution | 评分分布 |
| otherAsins | 关联 ASIN |
| deliveryTime | 发货时间 |
| category_id | 类目 ID |
| category_name | 类目名称 |
| pkg_dims | 包裹尺寸 |
| pkg_weight | 包裹重量 |
| product_dims | 商品尺寸 |
| product_weight | 商品重量 |
| first_date | 上市时间 |
| bestSellersRank | 热卖排名 |
| productDescription | 商品描述 |
| highResolutionImages | 高清图 |
| galleryThumbnails | 缩略图 |
| aiReviewsSummary | AI 总结 |
| reviews | 客户评论 |
| attributes | 商品属性 |
| productOverview | 产品概述 |
| variantDetails | 变体详情 |
| parentAsin | 父级 ASIN |

#### amzKeyword（关键词搜索）

| 字段 | 说明 |
|---|---|
| asin | ASIN 码 |
| title | 商品标题 |
| price | 商品价格 |
| star | 商品评分 |
| rating | 评分数 |
| image | 图片链接 |
| sales | 商品销量 |
| rank | 自然排名 |
| sponsored | 是否 SP 广告 |
| spRank | SP 广告排名 |
| badge | 徽章 |
| delivery | 发货时间 |

#### amzProductOfCategory（类目商品列表）

| 字段 | 说明 |
|---|---|
| asin | ASIN 码 |
| title | 商品标题 |
| price | 商品价格 |
| star | 商品评分 |
| rating | 评分数 |
| image | 图片链接 |

#### amzProductOfSeller（卖家商品列表）

| 字段 | 说明 |
|---|---|
| asin | ASIN 码 |
| title | 商品标题 |
| price | 商品价格 |
| star | 商品评分 |
| rating | 评分数 |
| image | 图片链接 |

#### amzBestSellers（热销榜）

| 字段 | 说明 |
|---|---|
| asin | ASIN 码 |
| rank | 榜单排名 |
| title | 商品标题 |
| price | 商品价格 |
| star | 商品评分 |
| rating | 评分数 |
| image | 图片链接 |

#### amzNewReleases（新品榜）

| 字段 | 说明 |
|---|---|
| asin | ASIN 码 |
| rank | 榜单排名 |
| title | 商品标题 |
| price | 商品价格 |
| star | 商品评分 |
| rating | 评分数 |
| image | 图片链接 |

</details>

### Amazon Review API：通用参数

文档：<a href="https://docs.pangolinfo.com/en-api-reference/amazonReviewAPI/submit?referrer=github_amz" target="_blank" rel="noopener noreferrer">https://docs.pangolinfo.com/en-api-reference/amazonReviewAPI/submit</a>

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

文档：<a href="https://docs.pangolinfo.com/en-api-reference/universalApi/universalApi?referrer=github_amz" target="_blank" rel="noopener noreferrer">https://docs.pangolinfo.com/en-api-reference/universalApi/universalApi</a>

- URL：`POST https://scrapeapi.pangolinfo.com/api/v1/scrape/batch`
- 参数：`urls[]`、`format (rawHtml|markdown)`、可选 `timeout`（毫秒）

### Amazon Niche Data API：通用参数

本仓库实现的 Niche Data 端点全部来自官方 Playground：

- <a href="https://docs.pangolinfo.com/en-api-reference/browseCategoryTreeAPI/submit?referrer=github_amz" target="_blank" rel="noopener noreferrer">Category Tree API</a>
- <a href="https://docs.pangolinfo.com/en-api-reference/searchCategoriesAPI/submit?referrer=github_amz" target="_blank" rel="noopener noreferrer">Search Categories API</a>
- <a href="https://docs.pangolinfo.com/en-api-reference/batchCategoryPathsAPI/submit?referrer=github_amz" target="_blank" rel="noopener noreferrer">Batch Category Paths API</a>
- <a href="https://docs.pangolinfo.com/en-api-reference/categoryFilterAPI/submit?referrer=github_amz" target="_blank" rel="noopener noreferrer">Category Filter API</a>
- <a href="https://docs.pangolinfo.com/en-api-reference/nicheFilterAPI/submit?referrer=github_amz" target="_blank" rel="noopener noreferrer">Niche Filter API</a>

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

## 🎉 立即开始

不要犹豫，立即获取您的免费资源！

- ⭐ 给项目点个 Star
- 📱 添加微信：Pangolin-Scraper（备注：GitHub 免费测试）
- 💬 WhatsApp（备注：GitHub 免费测试）

<table>
  <tr>
    <td align="center">
      <img src="images/wechat-qrcode.png" alt="微信二维码：Pangolin-Scraper" width="220">
      <br>
      微信：Pangolin-Scraper
    </td>
    <td align="center">
      <img src="images/whatsApp.webp" alt="WhatsApp 二维码" width="220">
      <br>
      WhatsApp：GitHub 免费测试
    </td>
  </tr>
</table>

- � 开始您的数据采集之旅

让数据采集变得简单，让开源精神传递！ 🌟
