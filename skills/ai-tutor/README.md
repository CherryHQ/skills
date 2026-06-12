# 🤖 AI Tutor — CherryStudio Skill

> 原项目 [AI-Learning-Tutor](https://github.com/ninime09/AI-Learning-Tutor) 的 CherryStudio 适配版。

一个面向 AI 初学者的 CherryStudio Agent Skill，自动抓取 Anthropic、OpenAI、Cursor 等大厂最新博客，生成结构化深度精读笔记，直接存入 CherryStudio 笔记目录。

---

## ✨ 与原版差异

| 原版（Claude Code + Obsidian） | CherryStudio 版 |
|---|---|
| 依赖 `defuddle-cli` | 使用内置 `mcp__exa__web_fetch_exa` |
| 依赖 MCP `obsidian-vault` | 使用原生 `Write/Read/Glob/Bash` |
| 依赖 MCP `mcp-server-fetch` | 使用内置 `mcp__exa__web_search_exa` |
| 输出到 Obsidian Vault | 输出到 CherryStudio 笔记面板 |
| Obsidian callout 语法 | 纯 Markdown，完全兼容 |
| Obsidian wikilink `[[]]` | 书名号引用 |
| 需手动配置路径 | **开箱即用** |

## 📄 生成笔记结构

```
📌 核心速递      → 一句话说清楚这篇文章讲了什么
💡 术语百科      → ≥3 个专业术语的大白话解释
🚀 前沿速递      → 本文核心发布内容（新模型/新功能/新研究）
🛠️ 核心原理解析  → 现象→背景→原理→意义，含关键图表 + 导读
🧠 学习重点      → 3 个初学者最应带走的 Takeaways
🔍 关联思考      → 与 CherryStudio 笔记知识库中已有笔记的连接
📰 简报区        → 其他来源今日最新动态
```

## 🚀 安装方法

本 Skill 已为 CherryStudio 环境预配置，无需额外安装依赖。

### 方法一：直接安装

1. 下载本仓库的 `SKILL.md`
2. 在 CherryStudio 中使用技能管理器导入

### 方法二：手动安装

```bash
# 将 SKILL.md 复制到 CherryStudio Skills 目录
cp SKILL.md ~/Library/Application\ Support/CherryStudio/Data/Skills/ai-tutor/

# CherryStudio 会自动识别新技能
```

## 📖 使用方法

在 CherryStudio 对话中直接输入：

```bash
/ai-tutor              # 读 Anthropic Engineering 最新文章（默认）
/ai-tutor openai       # 读 OpenAI Blog 最新文章
/ai-tutor cursor       # 读 Cursor Blog 最新文章
```

生成的笔记自动出现在 CherryStudio 左侧「笔记」面板：
```
Notes/
├── AI_Learning/
│   └── 2026-03-02-文章标题.md         ← 精读笔记
├── AI_Learning_attachments/
│   └── 2026-03-02-anthropic-架构图.png ← 关键图表
└── .ai-tutor-read-log.md              ← 已读追踪
```

## 🛠️ 支持的来源

| 来源 | 参数 | URL |
| --- | --- | --- |
| Anthropic Engineering | 默认 | https://www.anthropic.com/engineering |
| OpenAI Blog | `openai` | https://developers.openai.com/blog |
| Cursor Blog | `cursor` | https://www.cursor.com/blog |

欢迎提 PR 添加更多来源！

## 📋 依赖

| 工具 | 用途 | 状态 |
| --- | --- | --- |
| `mcp__exa__web_fetch_exa` | 网页内容提取 | ✅ CherryStudio 内置 |
| `mcp__exa__web_search_exa` | 搜索 fallback | ✅ CherryStudio 内置 |
| CherryStudio 原生 Read/Write/Glob/Bash | 文件操作 | ✅ CherryStudio 内置 |

**零额外安装，零配置。**

## 📁 文件结构

```
ai-tutor-cherry-studio/
├── SKILL.md                # Skill 定义文件（完整工作流程）
├── README.md               # 本文件
└── CREDITS.md              # 致谢与原项目信息
```

## 🤝 贡献

欢迎通过 Issue 或 PR 改进这个 Skill：

- 添加新的博客来源
- 优化笔记结构
- 改进术语提取逻辑
- 支持更多语言

## 📄 许可

MIT License — 与原项目保持一致。
