# Cherry Studio · 内部 Skills

这是 **Cherry Studio 团队内部共享的 Claude Code skills 仓库**。不限定某个产品线——Cherry Studio 客户端、Cherry Studio Enterprise、各类内部工具、日常工作流程，任何能被 skill 封装并提效的场景都欢迎进来。

> 👐 **欢迎大家把自己磨出来的好 skill 上传到这里。**
> 一份好 skill = 一次把工作流琢磨透 + 让全团队以后都省一次事。小到「整理周报」「改文案」，大到「系统测试协作」「代码审查」，都值得沉淀。

结构参考 [anthropics/skills](https://github.com/anthropics/skills)。

---

## 当前 Skills

| Skill | 用途 | 典型触发词 |
|-------|------|------|
| [test-and-report](skills/test-and-report/) | 陪用户手动测 staging，按规范把 bug 落到飞书多维表格 + GitHub issue 双轨 | `test and report` / `边测边报` / `开始系统测试` / `帮我测 cherry / express saas` / 贴飞书测试文档 + bitable |
| [prd-creator](skills/prd-creator/) | 跟 PM 讨论 cherry-studio 社区版需求 → 出中英对照 PRD review → 用户确认后建英文 GitHub issue（CherryHQ/cherry-studio）+ 自动加入 Project #3 + 设字段 | `建需求单` / `把这个需求建到 GitHub` / `新建 feature issue` / `draft an issue for...` |
| [transcript-to-content](skills/transcript-to-content/) | 把转录稿 / 会议录音 / 原始笔记转成可发布内容：多条社交帖子 或 单篇长文。自动核查专有名词、数字、ASR 误转，长稿走索引检索策略防止编造 | `写成文章` / `整理成一篇文章` / `把转录稿转成文档` / `把这个录音整理成帖子` / `write up this session` / `turn this talk into a blog post` |

_（请持续补充）_

---

## 适用范围

| 场景 | 举例 |
|------|------|
| 产品相关工作流 | 客户端/SaaS 测试、发版、PR 审查、文档协作 |
| 研发流程 | Issue 分诊、PRD 写作、代码审查、release notes 生成 |
| 运营/市场/PM | 周报、会议纪要、公众号排版、飞书群通知 |
| 日常办公 | 邮件起草、日程整理、飞书多维表格自动化 |
| 新人上手 | 环境配置向导、内部 repo 权限申请、knowledge-base 索引 |

只要你反复做、每次都略有卡顿的事，就是一个 skill 候选。

---

## 安装（三选一）

### 方式 1：symlink 单个 skill（推荐）

最轻量。克隆仓库后，把目标 skill 软链接到 `~/.claude/skills/`：

```bash
cd ~/code  # 你平时放代码的地方
git clone git@github.com:CherryInternal/skills.git
cd skills

# 单独启用某个 skill
ln -s "$(pwd)/skills/test-and-report" ~/.claude/skills/test-and-report
```

后续 `git pull` 就能同步最新版本。

### 方式 2：symlink 全部

```bash
cd ~/code/skills
for skill in skills/*/; do
  name=$(basename "$skill")
  ln -sfn "$(pwd)/$skill" ~/.claude/skills/"$name"
done
```

### 方式 3：复制（不跟随更新）

```bash
cp -R skills/test-and-report ~/.claude/skills/
```

装完在 Claude Code / Conductor 里用触发词直接调用。

---

## 前置依赖（多数 skill 会用到）

| 能力 | 检查 | 缺失时 |
|------|------|------|
| `lark-cli` | `lark-cli contact +get-user` 能返回当前用户 | 找内部 onboarding 文档按 `lark-shared` 指引认证 |
| `gh` CLI | `gh auth status` 已登录且有目标 repo 写权限 | `gh auth login` + 让 org admin 加你到相应 repo |
| `upload-img`（Cloudflare R2 图床） | `which upload-img` 返回 `~/.local/bin/upload-img` | 向内部运维索取脚本，或改走手动上传 |
| `claude-in-chrome` 扩展（陪测 / 浏览器类 skill） | Chrome 菜单里有 Claude 图标并 Connect 成功 | [claude.com/chrome](https://claude.com/chrome) 下载安装 |

---

## 添加新 Skill（欢迎 PR ❤️）

1. **本地实现并用几次** —— 先在 `~/.claude/skills/<name>/` 里做，跑顺了再沉淀
2. **放到 `skills/<name>/`** —— 目录名 = SKILL.md frontmatter 里的 `name`
3. **至少要有 `SKILL.md`**，YAML frontmatter 必含 `name` + `description`（description 是触发逻辑的核心）
4. **可选**：`references/`（长篇规程/配置）、`scripts/`（可执行）、`assets/`（模板/图标等）
5. **在本 README 的「当前 Skills」表格里加一行**
6. 提 PR

**心法**（少踩坑）：
- 用 Anthropic 的 `skill-creator` skill 起草 + 优化 description，触发命中率会高很多
- SKILL.md 控制在 500 行内；超长内容拆到 `references/`，SKILL.md 里用链接指过去
- 描述里写清楚"**什么时候用**"和"**什么时候不用**"（反向清单能有效防止误触发）
- 如果 skill 引用了 base_token / 私有 repo 名 / 内部 URL，留意保密范围（本仓库 private 一份没事，但不要拷到公开仓库）

**不确定选题？** 常见高价值方向：
- 把自己手工做 5 次以上的流程固化（写周报、改 schema、回邮件）
- 把团队反复问的"怎么做 X"沉淀成可调用的 skill
- 给某个外部 CLI / API 包一层便利层

---

## 协作约定

- **命名**：kebab-case，动词优先（`test-and-report`、`doc-review`、`wechat-crm`）
- **变更**：PR 走 review，merge 走 squash
- **废弃**：不用的 skill 打上 `description` 里加 `[DEPRECATED]` 前缀，而不是直接删——给同事留反应时间
- **更新破坏性变更**：CHANGELOG 写一下，触发词改了记得在 PR 描述里 flag

---

## 保密提醒

本仓库是 **internal / private**。skill 内可能包含 staging token、内部 repo 名、客户数据表结构、账号 open_id 等敏感信息。

- ❌ 不要把 skill 拷贝到公开仓库
- ❌ 不要在公开渠道（X / 公众号 / 博客）整段引用 skill 里的配置块
- ✅ 可以在内部飞书 / 内部文档里分享、讨论、抄作业
