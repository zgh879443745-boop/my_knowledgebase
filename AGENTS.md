# AGENTS.md — 知识库入口指南

> **任何接入此知识库的 AI Agent 必须在处理用户请求前首先阅读本文档。**
> 本文档由系统自动加载，是 Agent 的"入职第一页"。

---

## 🚨 第一步：阅读规则（强制）

本文件同目录下还有以下规则文件，处理任何请求前按顺序阅读：

| 顺序 | 文件 | 用途 |
|------|------|------|
| 1 | `SCHEMA.md` | 目录结构、文件命名、双库映射规则、抖音路由规则 |
| 2 | `WORKFLOW.md` | 抖音 SOP、AI热点 SOP、异常处理流程 |

所有文件路径均为 `D:\my_knowledgebase\` 下的相对路径。

---

## ⚡ 请求类型 → 处理流程 速查

| 用户请求 | 处理流程 |
|---------|---------|
| 发送抖音链接 + "合入知识库" | → [流程A：抖音视频处理](#流程a抖音视频处理) |
| "帮我把这段文字记到知识库" | → [流程B：快速笔记](#流程b快速笔记) |
| "采集AI热点" / "更新热点" | → [流程C：AI热点采集](#流程cai热点采集) |

---

## 流程A：抖音视频处理

### A1. 路由判断（先于一切）

收到抖音链接后，先判断目标库：

| 用户表述 | 目标库 | 写入路径 |
|---------|--------|---------|
| "上传到 **AI热点**" / "合入 **ai-hotspots**" | `ai-hotspots/` | `ai-hotspots/hotspots/` |
| **未指定** / "合入**个人**知识库" | `personal/` | `personal/notes/`（有子文件夹要求则创建） |

### A2. 环境检查

```powershell
py -3.10 --version
ffmpeg -version
```

### A3. 执行提取

```powershell
py -3.10 D:\my_knowledgebase\tools\douyin-to-obsidian\douyin_to_obsidian.py --link "链接"
```

### A4. 错字修正 → 用户确认

1. 加载 `tools/douyin-to-obsidian/text_corrections.json`
2. 应用修正规则 + 人工修正（**保留英文原名，不翻译**）
3. 展示修正后内容给用户，等待确认

### A5. 写入笔记（按模板）

确认后，按 [📝 笔记模板](#笔记模板) 格式写入：

- **文件命名**：`抖音-{全标题}-{作者}.md`
- **存放路径**：按 A1 路由规则决定
- **冲突检测**：同名文件存在时提示用户，确认后覆盖

### A6. 更新索引

- 更新 `index.md` 对应库的表格行
- 追加 `log.md` 操作记录

### ⚠️ Skill 无法运行时

**不得跳过步骤创建空壳笔记**。必须报告缺失依赖，或让用户提供文本。

---

## 流程B：快速笔记

用户说"帮我把这段文字记到知识库"时：

1. **理解内容**：分析用户提供的文字，提取标题、标签、核心观点
2. **缺失字段询问**：标题不明、标签缺失时先问用户
3. **写入路径**：默认 `personal/notes/`
4. **格式**：`{简短标题}.md`，非抖音内容不加"抖音-"前缀
5. **内容结构**：遵循 [📝 笔记模板](#笔记模板)，跳过"原始转录"段落

---

## 流程C：AI热点采集

执行 `D:\my_knowledgebase\ai-hotspots\fetch_aihot.py`，更新 `index.md` 热点段落。

---

## 📝 笔记模板

所有笔记必须包含以下结构（按需调整段落）：

```markdown
---
title: {标题}
tags: [标签1, 标签2]
source: {来源链接}
date: {内容日期}
author: {作者}
---

# {标题}

## 视频摘要

{一段话概括全篇，150字以内}

## 核心观点

### 观点一：{小标题}

{展开说明}

### 观点二：{小标题}

{展开说明}

## 笔记

- {关键要点1}
- {关键要点2}

## 标签

#标签1 #标签2

## 原始转录（Whisper，已修正）

{完整转录文本，仅抖音视频有此段落}

## 备注

- 来源链接：{url}
- 采集时间：{YYYY-MM-DD}
```

> 非视频内容（快速笔记）省略"原始转录"段落，其余结构保持一致。

---

## 📂 文件夹创建规则

| 知识库 | 规则 |
|--------|------|
| `personal/` | 用户主动要求创建子文件夹分类时 **允许**，否则默认 `personal/notes/` |
| `ai-hotspots/` | ❌ **绝对禁止** 新建一级文件夹，目录结构固定 |

---

## 📁 路径速查

| 用途 | 绝对路径 |
|------|---------|
| 知识库根目录 | `D:\my_knowledgebase` |
| 个人笔记 | `D:\my_knowledgebase\personal\notes\` |
| AI 热点 | `D:\my_knowledgebase\ai-hotspots\hotspots\` |
| 抖音 Skill | `D:\my_knowledgebase\tools\douyin-to-obsidian\` |
| 错字修正 | `D:\my_knowledgebase\tools\douyin-to-obsidian\text_corrections.json` |

---

## ⛔ 禁止操作

- ❌ 抖音内容在用户未指定时写入 `ai-hotspots/`
- ❌ AI 资讯写入 `personal/`
- ❌ 跳过 `douyin-to-obsidian` Skill 手工创建抖音笔记
- ❌ 未经用户确认覆盖已有文件
- ❌ 跳过 `index.md` 和 `log.md` 更新
- ❌ 创建无摘要/无观点的空壳笔记
- ❌ 未经用户明确要求，在 `personal/` 下自创文件夹
- ❌ 在 `ai-hotspots/` 下新建一级文件夹
- ❌ 翻译英文插件/产品名称（保留原名）

---

## 🛠️ 故障排查

| 问题 | 解决 |
|------|------|
| Skill 调用失败 | 确认 Python 3.10 + FFmpeg + pip 包（requests, openai-whisper, moviepy, imageio-ffmpeg, ffmpeg-python） |
| 转录乱码 | 检查并扩展 `text_corrections.json` |
| 链接失效 | 提示用户重新生成抖音分享链接 |
| 文件路径错误 | 使用绝对路径，反斜杠需转义 |
