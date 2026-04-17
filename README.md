# Cherry Claude Skills

内部共享的 Claude Code skill 集合，服务于 Cherry Studio / Cherry Studio Enterprise 的工作流（系统测试、文档协作、bug 收集等）。结构参考 [anthropics/skills](https://github.com/anthropics/skills)。

## 当前 Skills

| Skill | 用途 | 触发 |
|-------|------|------|
| [test-and-report](skills/test-and-report/) | 陪用户手动测 staging，按规范把 bug 落到飞书多维表格 + GitHub issue 双轨 | `test and report` / `边测边报` / `开始系统测试` / `帮我测 cherry / express saas` / 飞书测试文档 URL + bitable 链接 |

（后续 skill 陆续加入。）

## 安装（三选一）

### 方式 1：symlink 单个 skill

最轻量。克隆仓库后，把目标 skill 软链接到 `~/.claude/skills/`：

```bash
cd ~/code  # 你平时放代码的地方
git clone git@github.com:CherryInternal/claude-skills.git
cd claude-skills

# 单独启用某个 skill
ln -s "$(pwd)/skills/test-and-report" ~/.claude/skills/test-and-report
```

后续 `git pull` 就能同步最新版本。

### 方式 2：symlink 全部

```bash
cd ~/code/claude-skills
for skill in skills/*/; do
  name=$(basename "$skill")
  ln -sfn "$(pwd)/$skill" ~/.claude/skills/"$name"
done
```

### 方式 3：复制（不跟随更新）

```bash
cp -R skills/test-and-report ~/.claude/skills/
```

安装完可在 Claude Code / Conductor 中直接用触发词调用。

## 前置依赖（skill 共用）

| 能力 | 检查 | 缺失时 |
|------|------|-------|
| [`lark-cli`](https://github.com/lark-cli-internal) | `lark-cli contact +get-user` 返回当前用户 | 先在内部 onboarding 文档按 `lark-shared` 指引认证 |
| `gh` CLI | `gh auth status` 已登录且有目标 repo 写权限 | `gh auth login` + 让 org admin 加你到相应 repo |
| `upload-img`（R2 图床） | `which upload-img` 返回 `~/.local/bin/upload-img` | 向内部运维索取脚本，或改走手动上传 |
| `claude-in-chrome` 扩展（陪测类 skill） | Chrome 菜单里有 Claude 图标并 Connect 成功 | claude.com/chrome 下载安装 |

## 添加新 Skill

1. 本地在 `skills/<new-skill-name>/` 创建目录
2. 至少包含 `SKILL.md`（带 YAML frontmatter：`name` + `description`）
3. 需要时加 `references/`（长篇参考）、`scripts/`（可执行脚本）、`assets/`（模板资源）
4. 在本 README 的 Skills 表格里加一行
5. PR 过来

推荐用 `skill-creator` skill（Anthropic 官方）起草和优化 description。SKILL.md 控制在 500 行以内，超长内容拆到 `references/`。

## 许可 / 保密

本仓库为**内部资料**。部分 skill 引用了 staging token、内部 repo 名、内部表格结构；不要外发。

