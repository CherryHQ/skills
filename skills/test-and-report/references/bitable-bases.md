# 已知多维表格配置

## Cherry Studio 客户端（桌面版）系统测试

- **base_token**: `AdeDbC9VgaNkrEsXtk5cTMarn2e`
- **主表 table_id**（测试问题）: `tbl7eUvrbfM7XFqg`
- **URL**: https://mcnnox2fhjfq.feishu.cn/base/AdeDbC9VgaNkrEsXtk5cTMarn2e
- **对应 GitHub repo**: `CherryHQ/cherry-studio`（公开）

### 字段 ID

| 字段 | 类型 | ID | 备注 |
|------|------|----|----|
| 问题标题 | text | `fldNrOaPGd` | 主字段 |
| 问题描述 | text | `fldPLm4WIR` | 多行 |
| 示例图 | attachment | `fld7RbjUJg` | **独立上传** |
| 模块 | select | `fldJnWKno4` | 17 个 Cherry Studio 分类 |
| 问题分类 | select | `fldDdSGUOn` | Bug / 体验优化 |
| 优先级 | select | `fldNeu8G9i` | P0 / P1 / P2 |
| 状态 | select | `fldhPJ0Uh8` | 待确认 / 已确认 / 修复中 / 已修复 / 已验证 / 暂缓 / 不修复 |
| 负责人 | user | `fld534eZGs` | |
| 提交人 | user | `fldmS8UN6v` | |
| Issue | text(url) | `fldpJVuWJR` | 值写法: `[#xxx](url)` |
| 备注 | text | `fldR8WITmw` | |
| 创建时间 | created_at | `fld4kmTKsp` | 系统自动，只读 |

---

## Cherry Studio Enterprise (Express SaaS Staging)

- **base_token**: `IJQPbTzZhaObMQsuL5OcbaoBnag`
- **主表 table_id**（问题收集）: `tbl20SIk4B78Ydpg`
- **URL**: https://mcnnox2fhjfq.feishu.cn/wiki/PkuVwDh42iQB3bkLGEdcndVJnuf?table=tbl20SIk4B78Ydpg
- **Staging 访问地址**: https://cse-admin-staging.cherry-ai.com
- **对应 GitHub repo**: `CherryInternal/cherry-studio-enterprise-api`（私有，前端在 `apps/admin/`，当前开发分支 `saas`）

### 字段 ID

| 字段 | 类型 | ID | 备注 |
|------|------|----|----|
| 问题标题 | text | `fldrugZmSN` | 主字段 |
| 问题描述 | text | `fldQnTONZx` | 多行 |
| 示例图 | attachment | `fldm170GcF` | **独立上传** |
| 模块 | select | `fldwb6HCeQ` | 目前只有"其他"占位，模块列表待定 |
| 问题分类 | select | `fldcR76H92` | Bug / 体验优化 |
| 优先级 | select | `fldWyNzv8J` | P0 / P1 / P2 |
| 状态 | select | `fld2ASTnm3` | 待确认 / 已确认 / 修复中 / 已修复 / 已验证 / 暂缓 / 不修复 |
| 负责人 | user | `fldB6FJWuS` | |
| 提交人 | user | `fldu4WcRMt` | |
| Issue | text(url) | `flds0thliZ` | 值写法: `[#xxx](url)` |
| 备注 | text | `fldvfYdQpr` | |
| 创建时间 | created_at | `fldkJquZgQ` | 系统自动，只读 |

---

## 视图速查（两个 Base 通用）

- **全部 - 按优先级**（默认）：grid，按优先级分组
- **P0 待修复**：grid，过滤 优先级=P0 且 状态 不在 (已修复/已验证/不修复)
- **按模块分组**：grid，按模块分组
- **状态看板**：kanban，按状态分组
- **已归档**：grid，过滤 状态 在 (已修复/已验证/不修复)

---

## 如果不是上述两个 Base

用户给的表不在清单里时：

1. 先从 URL 里拆出 wiki_token 或 base_token（`/wiki/...` 要先走 `lark-cli wiki spaces get_node --params '{"token":"<wiki_token>"}'` 拿 `obj_token`）
2. `lark-cli base +table-list --base-token <token>` 找到目标表
3. `lark-cli base +field-list --base-token <token> --table-id <tbl>` 拿字段 ID 清单和 options 枚举
4. 动态适配：字段名匹配、必填字段通过 description 里的"必填: 是"判断

**字段命名约定**（跨 Base 保持一致，便于模糊匹配）：
- 主字段一般叫"问题标题"或"Title"
- 多选单选字段用中文（问题分类/优先级/状态/模块）
- 附件字段叫"示例图"或"截图"或"attachments"
- 人员字段"提交人"/"负责人"
- URL 字段"Issue" 或 "Issue Link"
