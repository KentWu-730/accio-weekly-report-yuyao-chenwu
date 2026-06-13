# Accio Markdown 分享站

这个仓库里已经准备好了一个可直接发布到 GitHub Pages 的静态站点，用来给客户上传并查看 Markdown，电脑端和手机端分别走不同入口。

## 发布目录

- `site/index.html`：电脑端入口，上传 `.md` 并渲染
- `site/weekly_report/latest.html`：手机端最新周报渲染页
- `site/md-viewer.html`：电脑端公开 Markdown 渲染器

## 周报脚本的固定执行路径

周报任务的唯一推荐执行方式是：

```bash
./refresh-weekly-report.sh
```

这条路径会调用 `sync_weekly_reports.py --finalize-weekly-review`，并把以下动作收口到同一条链路里：

- 镜像周报结果到仓库的 `output/weekly_report`
- 生成 / 刷新 `latest.md`
- 刷新 public-link 元数据
- 重新构建 GitHub Pages 站点

如果需要先做授权预检，`sync_weekly_reports.py` 也支持 `--require-auth`，但它只是前置检查，不是最终完成条件。

如果定时任务发现 `output/current_auth_state.json` 缺失，脚本会输出 `output/current_auth_state.request.md` 里的重新授权提示，方便你直接把这段口令发给 Accio。

建议的状态文件结构：

```json
{
  "authorized": true,
  "connected": true,
  "authorized_at": "2026-06-10T00:00:00+08:00",
  "account_id": "Alibaba.com account id",
  "account_name": "Alibaba.com account name",
  "scope": "alibaba.com"
}
```

## 生成站点

一个命令就够：

```bash
python3 build_github_pages_site.py
```

如果你只更新了 `output/weekly_report/*.md`，想顺手把网页和钉钉通知一起刷新，可以直接运行：

```bash
./publish-weekly-report.sh
```

## 发布到 GitHub Pages

仓库已经带了 GitHub Actions 自动发布流程：

1. 把仓库推到 GitHub 的 `main` 分支。
2. 在仓库设置里打开 Pages，并把 Source 设为 `GitHub Actions`。
3. 以后只要更新 `site/**`、`output/**` 或重新生成站点，推送后会自动发布。
4. 发布完成后，客户直接访问生成的 `github.io` 地址即可。

## 说明

- 这个站点不依赖自定义域名，先用免费的 `github.io` 地址就够。
- 如果以后你要换域名，可以再绑定自定义域名。
- `site/index.html` 是电脑端入口，客户可以直接上传 `.md` 并查看渲染结果。
- `site/weekly_report/latest.html` 是手机端最新周报渲染页。
- `site/md-viewer.html` 是电脑端公开渲染器，客户可以直接上传 `.md` 并查看渲染结果。
- 当前周报对外固定入口是：
  - `https://kentwu-730.github.io/weekly-report-share/md-viewer.html`
  - `https://kentwu-730.github.io/weekly-report-share/weekly_report/latest.html`
- `site/` 是最终发布产物，GitHub Actions 会自动从这里部署。
- `build_github_pages_site.py` 会自动同步周报并产出可发布目录。
- `publish-weekly-report.sh` 会在重建后自动把最新链接发到通知通道；如果本机存在 `accio-dingtalk-notify`，会优先走 Accio 通道，否则回退到 webhook。

## 备用发布方式

如果你之后需要迁移到 Cloudflare Pages，可以继续使用这条命令：

```bash
npx --yes wrangler pages deploy site --project-name accio-weekly-report-share
```

Cloudflare 这条线只作为备选，不是当前主发布路径。当前主路径仍然是 GitHub Pages。

## 上传到国内静态站时的目录

把 `site/` 目录整体上传即可。站点入口文件是：

- `site/index.html`：电脑端入口
- `site/weekly_report/latest.html`：手机端最新周报渲染页
- `site/md-viewer.html`：电脑端公开 Markdown 渲染器
