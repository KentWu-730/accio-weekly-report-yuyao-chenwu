# 当前授权状态写入规则

在网页端完成首次登录和授权后，Accio 需要把授权状态写入 `output/current_auth_state.json`。

建议结构：

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

要求：
- `authorized` 或 `connected` 至少有一个字段明确为真值
- 定时任务每次开始前都要先检查这个文件
- 如果文件不存在、损坏或显示未授权，先停止，不要继续跑周报
- 授权恢复后再继续执行，不要自动猜测账号状态
