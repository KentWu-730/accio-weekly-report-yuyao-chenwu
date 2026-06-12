# Windows 店铺上下文写入规则

这是给 Windows 机器用的桥接模板。不要直接复用 Mac 的路径。

请在 Windows 机器上把下面 6 个字段写到 `output/current_shop_context.json`：

```json
{
  "web_shop_id": "网页端店铺ID",
  "web_shop_name": "网页端店铺名",
  "accio_pair_shop_id": "Accio配对店铺ID",
  "accio_pair_shop_name": "Accio配对店铺名",
  "report_source_dir": "D:/Accio/shops/your_shop/reports",
  "report_output_dir": "D:/Accio/shops/your_shop/output"
}
```

字段要求：
- `web_shop_id` 和 `accio_pair_shop_id` 必须是一一对应的同一店铺
- `web_shop_name` 和 `accio_pair_shop_name` 要和实际显示名称一致
- `report_source_dir` 要指向 Windows 上真实的周报源目录
- `report_output_dir` 要指向 Windows 上真实的输出目录

填写规则：
- 网页端切店后，先确认当前网页店铺
- 再确认 Accio 里对应的配对店铺
- 两边不一致时，不要继续跑周报
- 任一字段变化，都要整份 JSON 重写
- 不要把 Mac 的 `/Users/...` 路径带进 Windows

定时任务前置检查：
- 先确认 `output/current_auth_state.json` 存在且显示已连接 / 已授权
- 再确认 `output/current_shop_context.json` 存在且字段完整
- 任一文件缺失、损坏、字段不全，都先停下，不要继续自动化

如果你要把这份发给 Windows 侧 Codex，直接告诉它：
- 先读取本机 Accio 的店铺映射状态
- 再生成 Windows 版 `current_shop_context.json`
- 不要修改 Mac 侧文件
- 不要猜店铺 ID 和目录
