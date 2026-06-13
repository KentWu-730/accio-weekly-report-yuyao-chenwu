# Accio Work Automation Prompts

## Daily International Station Diagnostic

```text
Before any analysis, you must first retrieve the actual Alibaba.com International Station store and industry data for the requested date range.
Hard requirements:
1. State the data source and date range you used. Use America/Los_Angeles (US Pacific Time) for all daily and weekly boundaries unless the backend explicitly exposes a different canonical shop timezone.
2. Quote the key raw fields you relied on before giving conclusions.
3. If any required metric is missing, say "data not retrieved" and stop. Do not guess, infer, or fabricate numbers.
4. Only after data retrieval, output today's diagnostic and optimization plan.
5. Identify undercovered keywords with real opportunity.
6. List products that should be optimized first.
7. For each product, give title, selling point, and keyword optimization suggestions.
8. Output the top 3 actions to execute today.
9. Keep the result structured, concise, and directly actionable.
```

## Daily Keyword Mining

```text
Before mining keywords, retrieve the actual Alibaba.com International Station store and industry data for today.
Hard requirements:
1. State the data source and date range used. Use America/Los_Angeles (US Pacific Time) for the daily boundary unless the backend explicitly exposes a different canonical shop timezone.
2. Quote the raw keyword and performance fields that support your output.
3. If the data cannot be retrieved, respond with "data not retrieved" and do not continue.
4. Focus on:
   - Keywords not yet covered by current titles
   - Keywords with high search growth
   - Buyer-intent keywords with strong conversion potential
   - Phrases useful for titles, detail pages, and ads
   - Prioritized keywords for immediate optimization
5. Output one keyword cluster per line.
```

## Daily Product Cleanup

```text
Before reviewing products, retrieve the actual Alibaba.com International Station store and product performance data.
Hard requirements:
1. State the data source and date range used. Use America/Los_Angeles (US Pacific Time) for the daily boundary unless the backend explicitly exposes a different canonical shop timezone.
2. Quote the raw product metrics that support your classification.
3. If the required product data cannot be retrieved, say "data not retrieved" and stop.
4. Only then classify products into keep, upgrade, or delete.
Rules:
1. Zero effect for 30 days and no engagement -> cleanup candidate
2. Historical clicks or feedback -> upgrade candidate
3. Inactive and zero performance -> delete candidate
4. Low-quality product -> detail page upgrade candidate
5. Output a concise action list with priorities.
```

## Weekly Shop Review

```text
请按当前 `SKILL.md` 执行周复盘。必须基于最近一个已完整结束的自然周，统计边界使用 America/Los_Angeles（美国太平洋时间）；如果当前周尚未结束，必须明确排除半周数据。正文必须全部使用中文，不能输出简略摘要，必须保持详细、运营化、可执行的结构。周复盘结束后必须运行 `refresh-weekly-report.sh`，确保 `latest.md`、公共链接元数据和站点页面一起刷新。不要依赖旧报告、临时目录或旧链接；只以当前最新生成的周报为准。
```

## Monthly Store Diagnostic

```text
Before running the diagnostic, retrieve the actual Alibaba.com International Station store, ad, and product data for the month.
Hard requirements:
1. State the month range and the data sources used.
2. Quote the raw metrics you relied on.
3. If data retrieval fails, say "data not retrieved" and stop.
4. Use the strongest available data to evaluate:
   - Traffic
   - Exposure
   - Clicks
   - Conversion
   - Product quality
   - Store vitality
   - Cleanup risk
5. Then output the red/yellow/green board, core bottlenecks, product cleanup list, and action plan.
```

## Competitor Title Decomposition

```text
Please decompose the following competitor titles into reusable keyword roots and high-value phrases.
Then rebuild them into a new high-conversion title matrix.
Rules:
1. Each extracted phrase should contain no more than 5 words.
2. Then output 15 to 20 new titles.
3. Keep each title within 110 to 120 characters and never exceed 128 characters.
4. Use Title Case.
5. Do not use punctuation.
6. Do not repeat the same word inside one title.
7. Output one line per item, with no extra explanation.
8. Do not include the correct brand name of any third-party brand in the title.
9. If compatibility must be mentioned, use generic safe wording only.
```

## Product Keyword to Title Matrix

```text
Please generate a title matrix from this product keyword.
Rules:
1. Output 15 to 20 titles.
2. Keep each title within 110 to 120 characters and never exceed 128 characters.
3. Use Title Case.
4. Do not use punctuation.
5. Do not repeat the same word inside one title.
6. Reuse the core keyword root, but vary modifiers, scenes, and intent terms.
7. Output one line per title, with no explanation.
8. Do not include the correct brand name of any third-party brand in the title.
9. If compatibility must be mentioned, use generic safe wording only.
```
