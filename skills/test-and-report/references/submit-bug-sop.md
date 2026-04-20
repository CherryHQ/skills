# Bug 提交 SOP（多维表格 + GitHub issue 双轨）

本文档是 `cherry-test-session` skill Phase 4 的详细规程。每条 bug 都必须完整执行所有 6 个环节，顺序不能颠倒。

---

## 1. 入口前置条件

进入本 SOP 之前，确保已经有一个"证据包"：

- 现象一句话（用户原话）
- 触发条件 / 复现步骤
- 环境信息（OS / 浏览器 / 版本 / 登录状态）
- 至少一项客观证据（截图 / Console 错误 / 网络请求 / DOM state）
- （可选）代码层根因

证据不齐 → 先回 Phase 3 补齐，不要带着半拉证据进 SOP。

---

## 2. 查重（必做，5 类处置）

### 2.1 提取关键词

从现象里挑最具体的 2-3 个关键词（报错码、组件名、函数名、文件路径、关键堆栈），**不要**用整句话搜。

### 2.2 搜索 3 个地方

**① 飞书多维表格**：
```
lark-cli base +record-search --base-token <BASE> --table-id <TABLE> --json '{"keyword":"<关键词>","search_fields":["问题标题","问题描述","备注"],"limit":20}'
```

**② GitHub issue（open + closed 都要查）**：
```
gh issue list --repo <OWNER/REPO> --search '<关键词>' --state all --limit 20
```

**③ GitHub PR（open + merged 都要查）**：
```
gh pr list --repo <OWNER/REPO> --search '<关键词>' --state all --limit 10
```

### 2.3 按 5 类处置

并排对比（现象 / 触发条件 / 平台 / 版本），归类到其中一类：

| 判断 | 证据特征 | 处置动作 |
|------|---------|---------|
| **完全相同的 open 条目** | 现象+触发条件+平台几乎一致，issue/record 未关闭 | **不要新建**。告诉用户「已有 #xxx / record <id>」，询问是追加信息还是取消 |
| **已修复的相同 Issue**（closed `✅fixed`） | 现象一致但 issue 已关闭且带修复标签 | **可能是回归 bug**。告诉用户「#xxx 在 vX.X 已修复但现象重现，可能是 regression」，等用户决定是新建还是在旧 issue 补充 |
| **正在修复的 PR**（open 或 已合并未发布） | PR 明确引用了相关代码/issue，且未发布到当前环境 | 告诉用户「PR #yyy 已经在修，预计 vX.X 发布」；用户可选：新建跟踪条目、先等发版、或在 PR 下评论 |
| **相关但不同** | 现象近似但触发条件/模块/影响范围有明显差异 | 可以新建，但**必须双向引用**（bitable 备注里 `见 #xxx`、issue 正文里 `Related: #xxx`） |
| **无关联** | 搜索无命中 | 正常走第 3 节 |

### 2.4 输出格式

搜完后发给用户一张汇总表：

```
关联搜索结果：

Bitable:
| record_id | 标题 | 状态 | 关系 |
| ...       | ...  | ...  | ...  |

GitHub Issue:
| #   | 标题 | 状态 | 关系 |
| ... | ...  | ...  | ...  |

GitHub PR:
| #   | 标题 | 状态 | 关系 |
| ... | ...  | ...  | ...  |

建议：{新建 | 追加到现有 | 先等 PR 发布}
理由：...
```

**铁律**：任何情况都先把表和建议展示给用户，**等明确指令才动作**。即使搜索无命中，也要问「未找到关联，确认新建？」不要自己判断直接建。

---

## 3. 定优先级（P0 / P1 / P2）

### 3.1 三档定义

| 档 | 定义 | 处理节奏 |
|----|------|---------|
| **P0** | 主路径阻塞 / 功能根本不可用 / 数据丢失 / 安全漏洞 | **必须立即改完** |
| **P1** | 比较严重的体验问题，主路径仍能走通但明显受损 | 后续马上处理（当前迭代内） |
| **P2** | 小的体验问题 / 非常低频遇到的问题 | 可以延后处理（排进队列） |

### 3.2 判断规则

1. **能从现象推断**（用户已说"走不通"、"崩溃"、"数据丢失" 等强信号）→ 直接填 + 在 Phase 4 Step 6 回报时简述理由方便用户推翻
2. **推断不了** → **必须**用 `AskUserQuestion` 弹 P0/P1/P2 三选项，问题文案：

   > 这条 bug 的优先级是？
   > - P0：主路径阻塞，必须立即改完
   > - P1：比较严重的体验问题，后续马上处理
   > - P2：小的体验问题 / 非常低频遇到的问题

3. **严禁**默认填 P1 或凭空猜——会污染统计和排期

---

## 4. 上传截图到 Cloudflare R2

```bash
upload-img <local-path-to-screenshot>
# 返回 https://pub-a9416c5573a34388b8d9465d8bef4257.r2.dev/YYYYMMDD/<filename>
```

- 脚本位置：`~/.local/bin/upload-img`
- Bucket：`screenshots`
- Key 格式：`YYYYMMDD/<原文件名>`（自动加日期前缀）
- 返回的是**公开 URL**，直接嵌入 GitHub issue 或分享

多张图分多次上传，拿到的 URL 逐个嵌入 issue 正文。

---

## 5. 写飞书多维表格

### 5.1 创建 record

```bash
lark-cli base +record-upsert \
  --base-token <BASE> \
  --table-id <TABLE> \
  --json '<record_json>'
```

**必填字段**：

| 字段 | 值格式 | 示例 |
|------|--------|------|
| 问题标题 | text (≤40 字摘要) | `"登录页发送验证码按钮首次加载禁用"` |
| 问题描述 | text（多行，含现象+环境+步骤+影响） | `"现象: ...\n环境: ...\n步骤: 1) ... 2) ..."` |
| 问题分类 | select 单选 | `"Bug"` 或 `"体验优化"` |
| 优先级 | select 单选 | `"P0"` / `"P1"` / `"P2"` |
| 状态 | select 单选 | **新提交默认 `"待确认"`**，不要擅自改后续态 |
| 提交人 | user | `[{"id":"ou_xxxxxx"}]`，通过 `lark-cli contact +get-user --jq .data.user.open_id` 取当前用户 |

**选填字段**：`模块`（Cherry Studio 客户端有 17 个 option，Express SaaS 暂只有"其他"）/ `Issue`（URL，写 `[#xxx](url)` 格式，表格只显示 #xxx 短超链接）/ `负责人`（人员）/ `备注`（多行）/ `示例图`（**不要塞进这里**，见下）

**不要写**：`创建时间`（系统自动）

### 5.2 值格式速查

| 字段类型 | JSON 值 |
|---------|---------|
| text | `"字符串"`（支持 `\n` 换行） |
| select 单选 | `"P0"`（字符串，精确匹配 option name） |
| user | `[{"id":"ou_xxx"}]` |
| text(url) | 推荐 `"[#129](https://.../issues/129)"` — 列内只显示 #129 可点；也接受纯 URL `"https://..."` |
| attachment | **走独立接口** `+record-upload-attachment` |
| created_at / updated_at | 不写 |

### 5.3 上传附件

**不能**塞进 upsert。拿到 record_id 之后单独调用：

```bash
lark-cli base +record-upload-attachment \
  --base-token <BASE> \
  --table-id <TABLE> \
  --record-id <record_id> \
  --field-id <示例图 field_id> \
  --file <local-path> \
  --name <display-name>   # 可选，默认用文件名
```

多张图分多次调用。

### 5.4 坑点

- `jq` 取 record_id 的路径是 `.data.record.record_id_list[0]`，**不是** `.data.record.record_id`（为 null）
- 单选值精确匹配大小写（`"p0"` 不行，必须 `"P0"`）
- 人员字段用 `{id: ...}` 包裹的数组，不是裸字符串

---

## 6. 创建 GitHub issue

### 6.1 标题格式

- 问题分类 = Bug → `[Bug]: <一句话问题摘要>`
- 问题分类 = 体验优化 → `[Feature]: <一句话改进摘要>` 或 `[Enhancement]: <...>`

### 6.2 正文格式（参考 `CherryHQ/cherry-studio#14338`）

```markdown
> [!NOTE]
> This issue was written in English by Claude. Original Chinese content is at the bottom.

### Pre-submission Checklist

- [x] I have searched existing issues and did not find a duplicate.
- [x] I have written a short, specific title.
- [x] I have provided reproduction information and root-cause analysis.

### Environment

- **URL**: <staging URL>
- **Branch**: `<branch>`
- **Commit**: `<short sha>` (as of <date>)
- **Platform**: <OS / browser>

### Summary

<One paragraph: symptom + reproducibility>

<img width="675" alt="<describe>" src="<R2 public URL>" />

### Root Cause

<Analysis with file:line references, code blocks for critical snippets>

### Why it races / Why it fails

<Mechanism explanation>

### Proposed Fix

<Tabular form preferred when changes map cleanly to rows (i18n keys, field copy, config values, enum additions):>

| Field | Label | Description | Placeholder |
|---|---|---|---|
| ... | ... | ... | ... |

<Otherwise a short numbered list of behavioral changes.>

**Files to touch:**
- `<path>:<line-range>` — <what changes>

### Out of scope

<Bulleted list of adjacent questions intentionally deferred (separate issue / product decision). Keeps this issue's scope bounded and prevents reviewers from expanding it.>

### Reproduction

<Step-by-step; include DevTools throttle settings if relevant>

### Related files

- `<file>:<line>` — <what's there>

---

<details>
<summary>原始中文内容 (Original Content)</summary>

### 现象
...

### 根因
...

### 建议修复
...

### 不在本 issue 范围
...

### 复现方式
...

</details>
```

### 6.3 创建命令

```bash
gh issue create --repo <OWNER/REPO> \
  --title '<title>' \
  --body-file <path-to-body.md>
```

### 6.4 打标签

**先看 repo 现有 label**，再决定用什么——不要凭空套 `type:*` 命名空间：

```bash
gh label list --repo <OWNER/REPO> --limit 100
```

按优先级挑 label：

1. **复用已有 label**：repo 里有 `bug` / `feature` / `BUG` / `enhancement` 这类语义对应的 label，直接用。
   ```bash
   gh issue edit <N> --repo <OWNER/REPO> --add-label "<existing>"
   ```
2. **没有语义对应**时才建新的：
   ```bash
   gh label create "type: bug" --color "d73a4a" --description "Functional defect (bitable: Bug)" --repo <OWNER/REPO>
   gh label create "type: feature" --color "0366d6" --description "UX improvement (bitable: 体验优化)" --repo <OWNER/REPO>
   ```

**已知仓库约定**：
- `CherryHQ/cherry-studio`（公开）：用老体系 `BUG`/`feature`/`P1`-`P3`，不要建 `type:*`。
- `CherryInternal/cherry-studio-enterprise-api`：当前实际使用 `bug` / `feature`（见 #135）。新建 `type:*` 前先 `gh label list` 确认没有语义重复的 label。

**优先级 label**（可选）：
- CherryHQ 有现成 `P1` / `P2` / `P3` label，bitable 的 P0/P1/P2 映射到 P1/P2/P3 或单独加 `P0`。
- enterprise-api 目前无优先级 label，需要的话同样 `gh label list` 确认后再建。

### 6.5 回填 Issue URL 到 bitable

```bash
lark-cli base +record-upsert \
  --base-token <BASE> \
  --table-id <TABLE> \
  --record-id <record_id> \
  --json '{"Issue": "[#<N>](<issue URL>)"}'
```

---

## 7. 回报给用户

固定格式：

```
✅ 已提交

标题: <问题标题>
分类: <Bug | 体验优化>  优先级: <P0 | P1 | P2>  状态: 待确认
record_id: <rec_xxx>
Issue: <GitHub issue URL>
Bitable: <base URL?table=tbl_xxx>

（若有）优先级判断理由: <一句话>
```

失败时透出错误码 + 原始 error message，不要隐藏。

---

## 8. 常见错误速查

| 错误 | 原因 | 处理 |
|------|------|------|
| `[800004135] OpenAPI* limited` | 飞书接口限流 | `sleep 2-5` 后重试，连发加间隔 |
| `[1254045]` 字段名不存在 | option name 拼错（`p0` vs `P0`） | `+field-list` 看真实 option |
| `[1254066]` 人员字段错误 | 直接写字符串或忘记 `{id: ...}` | 改为 `[{"id":"ou_xxx"}]` |
| 写入成功但示例图空 | 附件不能走 upsert | 用 `+record-upload-attachment` |
| `gh label create` 404 | 没 triage/write 权限 | 让用户给当前 GH 账号加权限 |
| `gh issue create` 成功但无 label | 同上 | 先建好 label 再重试 `edit --add-label` |
| JS tool `Cannot access a chrome-extension:// URL of different extension` | 页面有跨扩展 iframe (Geetest 等) | 降级：`read_page` + 看源码 |
