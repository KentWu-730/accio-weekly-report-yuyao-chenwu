# Cloudflare Pages 发布说明

目标：

- 不买域名
- 直接拿到免费 `*.pages.dev` 地址
- 公开页直接展示最新周报

## 说明

这条路径目前只是备用。当前主发布路径已经切到 GitHub Pages，Cloudflare 仅保留给未来迁移或对比使用。

## 已验证流程

1. 登录 Cloudflare。
2. 使用 `wrangler login` 完成 OAuth 授权。
3. 直接把 `site/` 目录部署到 Pages：

```bash
npx --yes wrangler pages deploy site --project-name accio-weekly-report-share
```

4. 复制 Cloudflare Pages 给你的默认 URL。
5. 把这个 URL 写进 `public_site_url.txt`，然后重新运行：

```bash
python3 build_github_pages_site.py
```

## 仓库里已经准备好的内容

- `site/index.html`
- `site/weekly_report/latest.html`
- `public_site_url.txt.example`

## 你现在要做的

如果要重新发布到 Cloudflare，先更新 `public_site_url.txt`，然后重新运行 `python3 build_github_pages_site.py`。这会同步：

- `site/index.html`
- `site/weekly_report/latest.html`
