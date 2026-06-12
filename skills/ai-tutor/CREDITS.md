# Credits

## 原始项目

本 Skill 基于 [AI-Learning-Tutor](https://github.com/ninime09/AI-Learning-Tutor) 改写而来。

- **原作者**: ninime09
- **原始许可**: MIT License
- **原始定位**: Claude Code Skill，输出到 Obsidian Vault

## CherryStudio 适配版改动

1. 网页抓取：`defuddle-cli` → `mcp__exa__web_fetch_exa`（CherryStudio 内置）
2. 文件系统：MCP `obsidian-vault` → CherryStudio 原生 `Write`/`Read`/`Glob` 工具
3. 搜索 fallback：MCP `mcp-server-fetch` → `mcp__exa__web_search_exa`（CherryStudio 内置）
4. 输出目标：Obsidian Vault → CherryStudio 笔记目录
5. 格式兼容：移除 Obsidian callout 语法 (`>[!abstract]`) 和 wikilink (`[[]]`)，改用纯 Markdown
6. 开箱即用：预设 CherryStudio 笔记默认路径，无需手动配置
7. 错误处理：针对 CherryStudio 工具链重写 error handling

适配工作由 CherryStudio Agent（CherryClaw）辅助完成。
