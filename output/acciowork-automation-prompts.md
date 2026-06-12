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
Temporary working directories are allowed for intermediate processing only. They must be treated as scratch space, not as the final source of truth.
The final weekly report must be written back to the canonical weekly report output directory. A report that exists only in a temporary directory does not count as complete.
The canonical completion path is `refresh-weekly-report.sh`, which must be run after report generation so the mirrored output, `latest.md`, and public-link metadata are refreshed together.
This task is only complete when all of the following are true:
1. The weekly report Markdown has been generated.
2. The Markdown file has been written to the canonical output directory.
3. latest.md has been updated to point to the newest weekly report.
4. The public-link metadata has been refreshed to match the newest report.
If the report exists only in a temporary directory, the task must be treated as incomplete and must not be declared successful.
After switching shops, the report must be regenerated from the active shop context and written back to the canonical output directory so the same links always open the latest weekly report for the currently active shop.

Before reviewing the week, retrieve the actual Alibaba.com International Station store backend, ad, and product data for the most recent fully completed natural week in America/Los_Angeles (US Pacific Time), defined as Sunday 00:00 to Saturday 23:59. If today is still inside the current natural week, do not use the partial current week for comparison; always report the last fully completed week as the main period.
Hard requirements:
1. State the exact week range and the data sources used.
2. Compare the main week against the previous fully completed week, not the partial current week.
3. When available, also compare against the average of the last 4 fully completed weeks.
4. Quote the raw metrics and source fields you used for the review.
5. If data retrieval fails, say "data not retrieved" and stop.
6. Do not infer trend direction without raw numbers.
7. Output:
   - Top changes this period
   - Keywords to add
   - Products to optimize
   - Next actions
8. If the current week has just started, explicitly say that the partial current week is excluded from the comparison.
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
