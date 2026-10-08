# AI 博主知识库 — 日志

> 追加写入，记录所有知识库操作（录入/查询/更新/冲突检测）
> 格式：`## [YYYY-MM-DD] 操作类型 | 描述`

---

## [2026-06-03] init | 知识库初始化
创建知识库目录结构，编写 SCHEMA.md、index.md、log.md。
基于 Karpathy/llm-wiki.md 模式，支持双知识库（个人+AI热点）。
配置 Horizon 作为 AI 信息收集系统。

## [2026-06-03] plan | 规划 Horizon 集成方案
- 克隆 Thysrael/Horizon 项目
- 配置中文输出
- 编写桥接脚本（Horizon 输出 → 知识库 Ingest）
- 配置定时 Lint（逻辑冲突检测）

## [2026-06-03] ingest | Horizon 首次采集成功
- 采集源：Hacker News、Reddit（r/LocalLLaMA、r/artificial）、RSS（Hugging Face Blog、OpenAI Blog）
- 采集时间范围：过去 24 小时
- 采集结果：29 条 → AI 分析后筛选 25 条（score ≥ 5.0）
- 输出文件：`horizon-2026-06-03-en.md`（14 KB，英文）
- 已导入到：`ai-hotspots/hotspots/AI热点-2026-06-03.md`
- 问题解决过程：
  - ❌ `.env` 文件 API 密钥前有多余空格 → ✅ 修复
  - ❌ `config.json` 模型名错误（`gpt-4o` → `deepseek-chat`）→ ✅ 修复
  - ❌ `orchestrator.py` 无条件调用 enrichment 导致卡死 → ✅ 注释掉
  - ✅ 最终成功生成摘要文件

## [2026-06-03] config | Horizon 配置更新
- `config.json` 添加 `ai.languages: ["zh"]`，下次采集将生成中文摘要
- `config.json` 关闭 `webhook`（未配置 URL）
- `config.json` 关闭 GitHub 源（避免 403）

---
## [2026-06-09] ingest | 抖音视频提取成功
- **视频链接**: https://v.douyin.com/3Pa-U3-HhLM/
- **视频标题**: 让Codex干活飞起 | Codex五大插件实测
- **视频作者**: 小韦用AI
- **视频ID**: 7646303972000681267
- **转录字数**: 1080 字
- **保存路径**: `personal/notes/codex_notes/抖音-让Codex干活飞起-小韦用AI.md`
- **使用工具**: `douyin-to-obsidian` Skill
- **AI摘要**: 五大插件（HyperFrame/Computer Use/Chrome/Slides/Coder）完整链路，覆盖动态页面→电脑操控→浏览器自动化→PPT生成→编程开发
- **索引更新**: ✅ 已更新 `index.md` 个人知识库段落
- **统计更新**: ✅ 个人笔记数 2 → 3

## [2026-06-09] ingest | 抖音视频存入 codex_notes 子目录
- **视频链接**: https://v.douyin.com/3Pa-U3-HhLM/
- **视频标题**: 让Codex干活飞起 | Codex五大插件实测
- **视频作者**: 小韦用AI
- **保存路径**: `personal/notes/codex_notes/抖音-让Codex干活飞起-小韦用AI.md`
- **修复**: codex_notes 从文件恢复为正确目录结构
- **索引更新**: ✅ 已更新 `index.md`
## [2026-10-08] moc | 创建 4 个 MOC 主题索引
- MOC-Agent → personal/mocs/MOC-Agent.md
- MOC-Codex → personal/mocs/MOC-Codex.md
- MOC-浏览器自动化 → personal/mocs/MOC-浏览器自动化.md
- MOC-AI学习路径 → personal/mocs/MOC-AI学习路径.md

## [2026-10-08] concept | 生成概念页 Agent
- 概念：Agent（智能体）
- 路径：concepts/Agent.md
- 依据：被 4 篇不同笔记引用，达到 ≥3 阈值

## [2026-10-08] graph-check | 图谱健康检查
- 报告：lint_reports/lint-graph-20261008.md
- 幽灵节点：28 个
- 孤立笔记：8 篇
- 主要问题：wikilink 使用简称，与精确文件名不匹配

## [2026-10-08] graph-repair | 统一修复图谱链接
- 修复范围：personal/notes/、personal/mocs/、concepts/
- 修复内容：将笔记简称统一为精确文件名，修复 `[[[[OpenConnector]]]]`，补建概念页 20 个
- 复检结果：幽灵节点 0 个，孤立 Markdown 笔记 0 篇
- 索引更新：✅ 已更新 `index.md` 概念索引与统计
