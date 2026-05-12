# 飞书多维表格参考（Base / Bitable）

> 本文件供参考查阅：auth 检查、配置常量、字段 schema。所有 Base 写入操作均通过 `scripts/invoice_intake.py` 执行，不要手动拼接 lark-cli 命令。

---

## 前提条件

执行任何飞书表格操作前，先确认 OAuth 已连接：

```bash
lark-cli auth status
```

如未连接：

```bash
lark-cli auth login --domain base,drive,sheets,contact
```

---

## 配置

| 配置项 | 值 |
|--------|-----|
| 汇总索引 Base Token | `JGzKb5SKSal9A3suMyRcxRepnLe` |
| 汇总索引表 ID | `tblavWeOwUGHQZhA` |

> 汇总表存储「姓名 → 个人报销 Base Token」映射，只读，不做写入。

---

## 个人报销表字段 Schema

字段以实际表结构为准，通过以下命令动态获取：

```bash
# 先定位个人 Base token（从汇总索引按姓名匹配）
lark-cli base +field-list \
  --base-token "<个人base_token>" \
  --table-id "<table_id>"
```

---

## 关键注意点

| 要点 | 说明 |
|------|------|
| 日期格式 | datetime 字段传**毫秒级** Unix 时间戳（秒 × 1000），传秒级会导致显示 1970 年 |
| 附件路径 | `+record-upload-attachment --file` 只接受相对路径，需先 `cd` 到文件目录 |
| 高级权限 | Base 开启高级权限时，应用/用户需有编辑权限，否则报 `91403 Forbidden` |
| select 字段 | 传选项名称字符串，区分大小写，必须与 Base 配置完全一致 |
| formula / auto_number | 只读，写入时跳过 |
