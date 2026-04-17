---
name: test-and-report
description: Coordinates a Cherry Studio / Cherry Studio Enterprise (Express SaaS) manual testing session where user explores a staging build and reports UX/bug findings. Parses the Feishu test doc for scope + code repo + bitable URL, sets up claude-in-chrome observation, captures environment evidence (DOM/console/network/screenshot) when user hits an issue, then files each finding to both the Feishu bitable (with attachments) and a GitHub issue (CherryHQ#14338 format, English-primary + Chinese, R2-hosted screenshots, correct type label). Enforces 5-way dedup triage (search bitable + GitHub issues + PRs first) and mandatory P0/P1/P2 priority prompt when unclear. Make sure to use this skill whenever the user says "test and report" / "边测边报" / "开始系统测试" / "帮我测 cherry / express saas" / "体验 staging" / "协作提 bug / 收集反馈", shares a Feishu testing doc, has a bitable URL open and wants to file a finding, or is about to file a UX/bug observation that needs both bitable + GitHub tracking. Do NOT use for: writing production Cherry Studio code, reviewing a PR, debugging CI failures, or general "how do I use Cherry Studio" questions — those go to code / PR-review / support workflows instead.
---

# Cherry 测试协作与 Bug 收集

把"飞书测试文档 → 浏览器抓证据 → 双轨提交（多维表格 + GitHub issue）"的全流程打包，保证每条反馈都带齐环境信息、截图、查重结论、优先级，落到两处可追踪。

## 触发边界（什么时候用、什么时候不用）

**用本 skill**：
- 用户发来飞书测试文档 URL（通常含测试范围 + 代码仓库 + 多维表格链接）
- 用户说"开始测 / 帮我测 / 体验 staging / 协作提 bug / 收集反馈"
- 用户描述一个 UX / 功能问题，并且要落到 bitable + GitHub 双轨
- 用户把已知的测试 bitable（如 `IJQPbTzZhaObMQsuL5OcbaoBnag` / `AdeDbC9VgaNkrEsXtk5cTMarn2e`）的 URL 发过来并提反馈

**不用本 skill**：
- 用户让你改 Cherry Studio 代码 / 提 PR → 走常规开发流程
- 用户让你 review 现有 PR → 用 `gh-pr-review` skill
- CI / 构建失败排查 → 用常规调试
- 用户问"Cherry Studio 怎么用 / 怎么下载" → 一般回答即可

---

## 前置检查（执行前先确认）

| 能力 | 检查方式 | 缺失时处理 |
|------|---------|-----------|
| claude-in-chrome 扩展 | `mcp__claude-in-chrome__tabs_context_mcp` 能返回 tab 列表 | 引导用户从 claude.com/chrome 安装并点 Connect，等"搞定"再继续 |
| lark-cli 已登录 | `lark-cli contact +get-user --jq .data.user.name` | 跳到 `lark-shared` skill 做认证 |
| gh CLI 有 repo 写权限 | `gh api repos/<OWNER>/<REPO> --jq .permissions` 里 `push` 为 true | 让用户给当前 GitHub 账号加 triage/write |
| R2 图床可用 | `which upload-img` 返回 `~/.local/bin/upload-img` | 手动降级：让用户把截图拖进 GitHub issue 编辑器 |

## 工作流总览

```
Phase 1  解析测试文档 (飞书 doc → 配置)
Phase 2  浏览器连接 (claude-in-chrome)
Phase 3  陪测：用户操作，agent 观察
Phase 4  每条 bug 的提交（查重 → 优先级 → 上传截图 → 多维表格 + GitHub 双轨）
Phase 5  回到 Phase 3 继续，直到用户说收工
```

---

## Phase 1: 解析测试文档

用户提供一个飞书文档 URL。用 `lark-cli docs +fetch --doc <URL> --format pretty` 拉全文，从中提取：

| 配置项 | 通常在文档哪里 |
|--------|--------------|
| **测试主题 / 范围** | 标题 + 开头段落 |
| **代码仓库**（GitHub URL） | "参考仓库" / "代码仓库" 段落，或正文里的 GitHub 链接 |
| **测试 staging URL** | "测试环境" / "访问地址" 段落 |
| **问题收集多维表格** | "问题收集" / "bug 列表" 段落里的 `mcnnox2fhjfq.feishu.cn/wiki/...?table=tbl...` 或 `/base/...?table=tbl...` |

**如果用户没给文档，只给了 bitable URL**：先识别是哪个产品（见下方自动识别规则），直接用 `references/bitable-bases.md` 的配置，staging URL 从 bitable 第一行记录或明确问用户。

### 自动识别当前产品

按下面的信号判断是哪个产品，从而知道用哪个仓库 + bitable：

| 信号 | 产品 | 仓库 | Bitable |
|------|------|------|---------|
| URL 含 `cse-admin-staging.cherry-ai.com` / `cherry-studio-enterprise-api` / "Express SaaS" / "Enterprise" | **Cherry Studio Enterprise** | `CherryInternal/cherry-studio-enterprise-api` | `IJQPbTzZhaObMQsuL5OcbaoBnag` / `tbl20SIk4B78Ydpg` |
| 提到"客户端" / "桌面版" / `github.com/CherryHQ/cherry-studio` / Electron | **Cherry Studio 客户端** | `CherryHQ/cherry-studio` | `AdeDbC9VgaNkrEsXtk5cTMarn2e` / `tbl7eUvrbfM7XFqg` |
| 都不明确 | 问用户 | — | — |

已知配置详情（包括字段 ID、枚举值、视图速查）见 `references/bitable-bases.md`。

---

## Phase 2: 浏览器设置

1. `tabs_context_mcp { createIfEmpty: true }` 检查连接
2. 没连上 → 引导用户装 claude-in-chrome 扩展（claude.com/chrome），装完点 Connect，再重试
3. 连上之后 `navigate` 到 staging URL
4. 顺手做一次基线采集（用户还没报 bug 之前）：
   - `read_page --filter interactive` 看主要交互元素
   - `read_console_messages` / `read_network_requests` 开始记录
   - （如有）记一下页面的核心脚本来源（第三方 captcha / CDN / 埋点）

**工具坑提醒**：
- `javascript_tool` 偶尔报 `Cannot access a chrome-extension:// URL of different extension`，通常是页面引了跨扩展 iframe（例如 Geetest）。遇到就降级靠 `read_page` + 读源码。
- `read_console_messages` / `read_network_requests` 需要页面加载时已在监听，建议刷新一次再读。
- 不要同时用 `chrome-devtools` MCP 的 debug 功能——会跟 claude-in-chrome 抢 Debugger 协议。

---

## Phase 3: 陪测循环

用户手动操作。agent 做两件事：

1. **被动观察**：不主动驱动用户，不乱点
2. **随叫随到**：用户说"这里有问题 / 点不动 / 报错了 / 看起来不对劲"立即采集证据

**证据包**（每条 bug 都至少收集）：

| 维度 | 工具 | 要点 |
|------|------|------|
| 现象描述 | 用户原话 | 一句话 + 复现触发条件 |
| DOM 状态 | `read_page`, `javascript_tool` | 关注按钮 disabled/pointerEvents/opacity/事件监听 |
| Console 错误 | `read_console_messages --pattern 'error\|warn\|Error'` | 只留 error/warn，不要全量 |
| 网络异常 | `read_network_requests --urlPattern '<接口前缀>'` | 找 4xx/5xx/pending |
| 截图 | 让用户 cmd+shift+4 截图到 `.context/attachments/`，或 `mcp__chrome-devtools__take_screenshot` | 报错场景必附；UX 类带"当前 vs 期望"更佳 |
| 代码层根因 | `gh api`/本地 grep | 有源码就看，找到按钮启用条件/API 路径/props gate |

证据齐了之后进 Phase 4。

---

## Phase 4: 每条 bug 的提交

详细规程见 `references/submit-bug-sop.md`。**高层步骤**（不要跳过）：

1. **查重**（必做，见 SOP 第 2 节）
   - 搜 bitable + GitHub issue（含 closed）+ GitHub PR（含 merged）
   - 命中后按 5 类处置：完全相同 / 已修复的 regression / 正在修的 PR / 相关但不同 / 无关联
   - 把对比表发给用户，等指令再动作——**无命中也要确认**

2. **定优先级**（见 SOP 第 3 节）
   - 能从现象推断 → 直接填 + 简述理由
   - 推断不了 → `AskUserQuestion` 弹 P0/P1/P2 三选项让用户选
   - **严禁**默认填 P1 或凭空猜

3. **上传截图到 R2**（见 SOP 第 4 节）
   ```
   upload-img <local-path>
   # 返回 https://pub-a9416c5573a34388b8d9465d8bef4257.r2.dev/YYYYMMDD/filename
   ```

4. **写飞书多维表格**
   - `+record-upsert` 必填：问题标题 / 问题描述 / 问题分类 / 优先级 / 状态(=待确认) / 提交人
   - `+record-upload-attachment` 把截图挂到 示例图 字段（**不能**塞进 upsert）

5. **创建 GitHub issue**
   - 标题：`[Bug]: <一句话>` 或 `[Feature]: <一句话>`（根据问题分类）
   - 正文按 `CherryHQ/cherry-studio#14338` 格式：英文正文在前（含翻译声明）、中文原文用 `<details>` 折叠、截图用 R2 URL 以 `<img src="...">` 嵌入
   - 打标签：问题分类 = Bug → `type: bug`；= 体验优化 → `type: feature`

6. **回报**：把 record_id、issue URL、bitable URL 三个链接一并给用户，外加一句总结"标题 / 分类 / 优先级 / 状态"

---

## Phase 5: 回到 Phase 3

用户继续测。每提一条 bug 就走一遍 Phase 4。

用户说"收工 / 测完了 / 今天到这 / 暂停"→ 输出本次 session 汇总：建了几条 record，几个 issue，有哪些 regression / 正在修的 PR 被识别，总共花了多久。

---

## 参考文件

- `references/bitable-bases.md` — 已知 Base token / 表 ID / 字段 ID / 选项枚举、跨 Base 的字段命名约定
- `references/submit-bug-sop.md` — 详细提交协议（查重 5 类处置、优先级规则、值格式、R2 上传、issue 模板）
