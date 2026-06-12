# 当前店铺上下文写入规则

Accio 在网页端切换店铺后，必须同时写入以下字段到 `output/current_shop_context.json`：

```json
{
  "web_shop_id": "网页端店铺ID",
  "web_shop_name": "网页端店铺名",
  "accio_pair_shop_id": "Accio配对店铺ID",
  "accio_pair_shop_name": "Accio配对店铺名",
  "report_source_dir": "D:/Accio/shops/shop_a/reports",
  "report_output_dir": "D:/Accio/shops/shop_a/output"
}
```

要求：
- `web_shop_id` 和 `accio_pair_shop_id` 必须能一一对应
- 任何一个值变化后，都要重写整个 JSON
- 周报脚本只认这个文件，不再靠手工输入店铺名
- 如果文件不存在或字段缺失，脚本回退到默认路径，但会导致串店风险

落地方式建议：
- 网页端切店后，先从网页端读取当前店铺 ID 和名称
- 再从 Accio 配对映射表里找到对应的 Accio 店铺 ID 和名称
- 把四个字段一起写入 JSON
- 再补上这家店自己的 `report_source_dir` 和 `report_output_dir`
- 周报脚本只读取这一个 JSON，保证网页店铺和 Accio 配对店铺是同一对

补充要求：
- 定时任务开始前，还要检查 `output/current_auth_state.json`
- 只有当授权状态文件明确表示已连接 / 已授权时，才允许继续跑周报
- 如果授权状态文件不存在、损坏或显示未连接，先停止并要求重新授权，不要直接跑任务
