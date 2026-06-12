# Accio Work Automation Prompts

## Weekly Shop Review

```text
Please review the most recent fully completed natural week of Alibaba.com International Station store performance, using store, ad, product, keyword, and industry data. Use America/Los_Angeles as the time boundary, with the reporting window fixed at Sunday 00:00 through Saturday 23:59. If today is still inside the current natural week, exclude the partial current week and analyze only the last fully completed week as the main period.

You must produce an operational weekly review, not a summary or a list of scattered conclusions:
1) Start with a weekly overview and explain the 3 to 5 most important changes, including the comparison baseline.
2) Compare the last fully completed week against the fully completed week before it, and if available also compare against the average of the last 4 fully completed weeks.
3) Include the core metrics in full, at minimum exposure, clicks, CTR, CPC, spend, business opportunities, inquiries, orders, conversion rate, business cost, daily budget consumption, and remaining budget.
4) Break down changes by traffic source, keywords, ad plans, and product level. Do not only state conclusions; explain causes and impact.
5) Clearly identify the fastest-growing item, the steepest decline, and the most abnormal product, traffic term, ad plan, or conversion stage.
6) For each key product, provide title, selling point, and keyword optimization suggestions. Provide at least 1 and at most 3 suggestions per product.
7) Explain anomalies, likely causes, risk assessment, and whether the behavior looks like cold-start or learning-period fluctuation.
8) End with next-week action recommendations sorted by priority. Include at least 5 actions and make them directly executable.
9) If a conclusion depends on a weak signal, label it as a "hypothesis" instead of a fact.
10) For every high-spend or highly abnormal plan, write it in the format "phenomenon -> cause -> recommended action -> expected impact".

The weekly report structure must be more complete. Use this order:
1. Weekly overview
2. Core KPI table
3. Traffic and channel analysis
4. Paid traffic / 全站推 analysis
5. Product analysis
6. Keyword analysis
7. Anomalies and causes
8. Next actions

The ad section must be expanded separately and must follow the real 全站推 logic. Do not reduce it to one sentence:
- business opportunity price / business cost / actual conversion cost
- daily budget / budget consumption / remaining budget / budget utilization
- spend, exposure, clicks, CTR, CPC
- business opportunities, inquiries, orders
- keyword-level and product-level acquisition efficiency
- high-spend low-conversion keyword sets, bid-up candidates, and downrank / negative-keyword candidates
- budget reallocation recommendations and bid adjustment recommendations for next week
- analyze only enabled / active plans; exclude disabled plans from the core judgment
- if a plan is in the first 7 days of learning, mark it as cold-start and avoid frequent bid, budget, product, or pause/resume changes
- if the campaign is a 全站推 plan, prioritize whether cost protection is active, ended, or invalid when that status is available
- describe the actual billing basis as clicks, and describe actual conversion cost as spend divided by 全站推 business-opportunity conversions
- if plan status is identifiable, break down the efficiency, budget utilization, and anomalies of each active plan
- if available, include query downranking, country bid multipliers, buyer bid multipliers, product exclusion, and country downranking suggestions
- if ad data is incomplete, clearly state the missing fields, the reason they are missing, and the effect on conclusions
- if an anomaly cannot be confirmed, write a hypothesis first, then the recommended action
- every core conclusion must be backed by the raw metric or data source

The output must be Markdown and directly saveable as `weekly_report_YYYY_WW.md`, written into `/Users/wukk/Documents/Accio-YuyaoChenwu/output/weekly_report`. When reading or reusing the latest report, always prefer the newest `.md` file in that directory. Do not add a public-links section, QR code text, or any fixed-share-page wording. Use the strongest available International Station store, ad, and product data, and do not turn the report into a vague summary or over-compress it.
```

## Monthly Store Diagnostic

```text
Please run a monthly diagnostic for the International Station store.
Use the strongest available data to evaluate:
1. Traffic
2. Exposure
3. Clicks
4. Conversion
5. Product quality
6. Store vitality
7. Cleanup risk
Then output the red/yellow/green board, core bottlenecks, product cleanup list, and action plan.
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
```
