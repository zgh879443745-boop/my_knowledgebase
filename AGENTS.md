# AGENTS.md - 知识库入口指南

> **任何接入此知识库的 AI Agent 必须在处理用户请求前阅读本文档。**

## 🚨 强制第一步

在处理任何请求之前，**必须按顺序读取以下文件**：

1. `SCHEMA.md` — 知识库结构、双库映射规则、文件命名规范
2. `WORKFLOW.md` — 抖音处理 SOP、热点采集 SOP、异常处理
3. `AGENT_ONBOARDING.md` — 环境检查清单、禁止操作

## 🔗 抖音链接处理（最高频操作）

当用户发送 `v.douyin.com` 链接并要求合入知识库时：

### 必须执行的标准流程

1. **检查环境**：`py -3.10 --version` 和 `ffmpeg -version`
2. **运行 Skill**：`py -3.10 D:\my_knowledgebase\tools\douyin-to-obsidian\douyin_to_obsidian.py --link "链接"`
3. **错字修正**：加载 `D:\my_knowledgebase\tools\douyin-to-obsidian\text_corrections.json` 并应用
4. **用户确认**：展示修正后的转录内容，等待用户确认
5. **冲突检测**：检查 `personal/notes/` 下是否存在同名文件
6. **写入笔记**：生成包含 frontmatter + 原始转录 + 摘要 + 核心观点的结构化笔记
7. **更新索引**：更新 `index.md` 和 `log.md`

### ⚠️ 如果 Skill 无法运行

若环境不满足（缺 Python 3.10 / FFmpeg / 依赖包），**不得跳过步骤直接创建空壳笔记**。必须：

- 向用户明确报告缺失的依赖
- 询问用户是否手动提供视频转录文本
- 或引导用户完成环境配置

## 📁 路径速查

| 用途 | 路径 |
|------|------|
| 知识库根目录 | `D:\my_knowledgebase` |
| 个人笔记 | `personal/notes/` |
| AI 热点 | `ai-hotspots/hotspots/` |
| 抖音 Skill | `tools/douyin-to-obsidian/` |
| 错字修正 | `tools/douyin-to-obsidian/text_corrections.json` |


## 📂 文件夹创建规则

| 知识库 | 规则 |
|--------|------|
| `personal/` | 用户主动要求创建文件夹分类时允许创建，否则默认合入 `personal/notes/` |
| `ai-hotspots/` | ❌ **绝对禁止**新建一级文件夹，目录结构固定不可更改 |

## ⛔ 禁止操作

- ❌ 抖音内容写入 `ai-hotspots/`
- ❌ AI 资讯写入 `personal/`
- ❌ 跳过 `douyin-to-obsidian` Skill 直接手工创建笔记
- ❌ 未经用户确认覆盖已有文件
- ❌ 跳过 `index.md` 和 `log.md` 更新
- ❌ 不提取视频摘要就创建笔记
- ❌ 未经用户明确要求，不得在 `personal/` 下自创文件夹
- ❌ 绝对禁止在 `ai-hotspots/` 下新建一级文件夹
