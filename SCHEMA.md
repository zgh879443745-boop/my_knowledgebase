# AI 博主知识库 — Schema

> 基于 Karpathy/llm-wiki.md 模式构建，由 AI Agent 自动维护，人类用 Obsidian 浏览。

## 知识库用途

为 AI 博主维护两个持久化知识库：
1. **个人知识库**（`personal/`）：管理用户自行输入的内容（笔记、想法、草稿、素材）
2. **AI 行业热点库**（`ai-hotspots/`）：定时自动收集 AI 行业热点信息，转化为中文存储

所有内容积累沉淀，避免重复查找，AI 自动维护，人类专注创作。

---

## 目录结构

```
MyKnowledge_base/
├── SCHEMA.md            ← 本文件：知识库结构与 AI 工作规则
├── index.md             ← 总索引（按分类组织，含链接+摘要）
├── log.md               ← 时间线日志（追加写入，AI 自动维护）
│
├── raw_sources/         ← 原始素材（用户投喂的链接/文本/视频，AI 不修改）
├── personal/            ← 个人知识库（用户自行输入的内容）
│   ├── notes/           ← 个人笔记
│   ├── drafts/          ← 博文草稿
│   └── ideas/           ← 选题想法
│
├── ai-hotspots/         ← AI 行业热点库（AIHOT 自动采集 + AI 整理）
│   ├── hotspots/        ← 热点条目（每个热点一个文件）
│   ├── concepts/        ← 概念解释页（AI 自动归纳）
│   ├── people/          ← 人物页（AI 自动创建）
│   ├── companies/       ← 公司/产品页（AI 自动创建）
│   └── daily/           ← 每日简报归档（AIHOT 输出）
│
├── concepts/            ← 跨库共享概念页（个人+热点共同引用）
├── timeline/            ← 时间线视图（按月份组织）
│
└── lint_reports/        ← 逻辑冲突检测报告（AI 定期生成）
```

---

## 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 抖音笔记 | `抖音-{全标题}-{作者}.md` | `抖音-让Codex干活飞起-小韦用AI.md` |
| 博文草稿 | `PD-{序号}-{标题}.md` | `PD-001-2026-ai-trend.md` |
| 选题想法 | `PI-{序号}-{标题}.md` | `PI-001-agent-framework-review.md` |
| AI 热点 | `AH-{YYYYMMDD}-{简短描述}.md` | `AH-20260603-gpt5-release.md` |
| 概念页 | `{概念名}.md` | `concepts/RAG.md` |
| 人物页 | `{人名}.md` | `ai-hotspots/people/李飞飞.md` |
| 公司页 | `{公司名}.md` | `ai-hotspots/companies/OpenAI.md` |
| 每日简报 | `YYYY-MM-DD.md` | `ai-hotspots/daily/2026-06-03.md` |

---


## 🎬 抖音视频路由规则

> 抖音视频通过 `douyin_to_obsidian.py` 提取后，按以下规则选择目标库：

| 用户表述 | 目标库 | 存放路径 |
|---------|--------|---------|
| "上传到**AI热点**" / "合入**ai-hotspots**" | `ai-hotspots/` | `ai-hotspots/hotspots/` |
| **未指定**目标库 / "合入**个人知识库**" | `personal/` | `personal/notes/`（有子文件夹要求则创建子文件夹） |

> ⚠️ 不可自行判断抖音内容属于哪个库，必须以上述规则为准。
## ⚡ 用户语义 → 目标库 映射规则（所有 Agent 必须首先阅读本节）

> **本规则适用于任何接入本知识库的 AI Agent 工具。**
> 用户在描述"合入知识库"时，必须根据以下语义判断目标库，不得自行猜测。

### 判断逻辑（优先级从高到低）

| 用户表述                      | 目标库               | 存放目录                    | index.md 段落 |
| ------------------------- | ----------------- | ----------------------- | ----------- |
| 含"**个人知识库**"或"**合入个人**"   | `personal/`       | `personal/notes/` 或子目录  | 🧠 个人知识库    |
| 含"**AI热点**"或"**合入热点**"    | `ai-hotspots/`    | `ai-hotspots/hotspots/` | 🔥 AI 行业热点库 |
| 内容来源为**抖音/小红书/B站**等个人社交媒体 | `personal/`       | `personal/notes/`       | 🧠 个人知识库    |
| 内容来源为**AI 行业资讯/论文/产品发布**  | `ai-hotspots/`    | `ai-hotspots/hotspots/` | 🔥 AI 行业热点库 |
| 无法判断时                     | **必须询问用户**，禁止自行决定 |                         |             |

### 禁止操作

- ❌ 不得将社交媒体个人内容合入 `ai-hotspots/`
- ❌ 不得将 AI 行业热点合入 `personal/`
- ❌ 不得跳过 `index.md` 更新步骤
- ❌ 不得在未确认目标库的情况下写入任何文件
- ❌ 不得在 `ai-hotspots/` 下新建一级文件夹（目录结构固定不可更改）

### 示例

| 用户说 | 正确操作 |
|-------|---------|
| "把这个抖音内容合入知识库" | 合入 `personal/notes/`，更新 index.md 个人知识库段落 |
| "合入AI热点" | 合入 `ai-hotspots/hotspots/`，更新 index.md AI 热点库段落 |
| "今天有什么 AI 热点" | 查询 `ai-hotspots/`，不查询 `personal/` |
| "我的笔记里有没有关于 RAG 的内容" | 查询 `personal/notes/`，不查询 `ai-hotspots/` |

---

## AI 工作流规则

### 0. 抖音视频处理 SOP (Standard Operating Procedure)

> **详细步骤参见 `WORKFLOW.md` 流程一**。
> **新人入职前必读 `AGENT_ONBOARDING.md`**。

**触发条件**：
- 用户发送 `v.douyin.com` 或 `douyin.com` 链接。
- 用户说"提取抖音"、"合入个人知识库"。

**强制规则**：
1. **必须使用 `douyin-to-obsidian` Skill**
   - 路径：`D:\my_knowledgebase\tools\douyin-to-obsidian\`
   - 脚本：`douyin_to_obsidian.py`
2. **必须应用错字修正**
   - 加载 `D:\my_knowledgebase\tools\douyin-to-obsidian\text_corrections.json`
   - 对 Whisper 转录结果执行自动替换。
3. **必须人工校验**
   - 展示修正后内容给用户，等待确认。
4. **必须检测重名冲突**
   - 若 `personal/notes/` 下存在同名文件，提示用户并展示旧内容。
   - 用户决定覆盖则替换，否则终止。

**详细操作步骤**：见 `WORKFLOW.md` "流程一"。

---

### 1. 个人内容录入（Personal Ingest）

**触发**：用户投喂内容（文本、链接、视频链接）

**流程**：
1. AI 读取原始内容
2. 判断内容类型（笔记/草稿/想法）
3. 创建对应文件到 `personal/` 子目录
4. 提取关键概念，更新 `concepts/` 中相关页面
5. 更新 `index.md`（个人知识库段落）和 `log.md`
**子目录规则**：
- 用户**主动要求**在 personal/ 下创建新文件夹（如 "codex_notes"）用于分类，则允许创建，内容合入该子目录
- 用户**未指定**文件夹时，默认合入 `personal/notes/`


**注意**：
- 抖音视频链接 **必须** 按 "0. 抖音视频处理 SOP" 执行。
- 其他视频链接（B站等）可参考抖音 SOP 流程。

---

### 2. AI 热点录入（AIHOT Ingest）

**触发**：AIHOT 定时任务运行 → 调用 `aihot.virxact.com/api/public/daily` → AI 整理入库

**流程**：
1. AIHOT API 采集原始信息（中英文混合，168 个信源）
2. **必须全部转化为中文**存储（人名/专业名词保留英文，附中文注解）
3. 每条热点必须附带**原始链接**（`sourceUrl` 字段）
4. 每条热点必须标注**采集时间**（`采集时间: YYYY-MM-DD HH:MM`）
5. AI 创建 `ai-hotspots/hotspots/AI热点-YYYY-MM-DD.md`
6. AI 更新关联的概念页、人物页、公司页
7. AI 更新 `index.md`（AI 热点库段落）和 `log.md`

**翻译规则**：
- 正文内容：全部中文
- 人名：英文原名 + 中文译名（如 `Yann LeCun（杨立昆）`）
- 技术名词：英文原名 + 中文解释（如 `RAG（检索增强生成）`）
- 公司名：中文通用名优先（如 `OpenAI` 可保留英文）

---

### 3. 查询（Query）

**触发**：用户提问

**流程**：
1. AI 先读 `index.md` 定位相关页面
2. 读取相关问题页
3. 综合回答，并注明信息来源和时间

---

### 4. 逻辑冲突检测（Lint）

**触发**：定时执行（建议每周一次）或用户手动触发

**检测内容**：
- **时间冲突**：同一事件在不同页面有不同日期
- **事实冲突**：同一概念在不同页面有矛盾描述
- **状态冲突**：某产品在同一时间既被描述为"已发布"又被描述为"未发布"
- **孤立页面**：有出链但无入链的页面
- **重复热点**：同一事件被录入多次

**冲突处理流程**：
1. AI 扫描所有页面，检测冲突
2. 生成冲突报告，写入 `lint_reports/lint-YYYYMMDD.md`
3. **等待用户反馈后解决**（不自动覆盖）
4. 用户确认后，AI 更新相关页面并标注修订日期

---

## 热点条目模板

```markdown
# AH-{YYYYMMDD}: {热点标题}

## 基本信息
- 采集时间: YYYY-MM-DD HH:MM
- 原始链接: [来源名称](URL)
- 热度评分: ⭐⭐⭐⭐⭐（1-5 星，AI 根据讨论度判断）
- 信息来源: HackerNews / Reddit / 论文 / 官方博客

## 事件摘要
{AI 用 3-5 句话概括，全部中文}

## 关键信息
- {要点 1}
- {要点 2}
- {要点 3}

## 相关概念
- [[RAG]]
- [[Agent]]

## 相关人物
- [[Yann LeCun（杨立昆）]]

## 相关公司
- [[OpenAI]]

## 标签
#热点 #技术突破 #产品发布 #LLM

## 状态
持续追踪 / 已结束 / 待验证

## 修订记录
- YYYY-MM-DD: 初始创建
- YYYY-MM-DD: {修订说明}
```

---

## 个人笔记模板

```markdown
# PN-{序号}: {笔记标题}

## 创建时间
YYYY-MM-DD

## 内容
{笔记正文，支持 Markdown 格式}

## 关联热点
- [[AH-20260603-gpt5-release]]

## 标签
#笔记 #RAG

## 状态
草稿 / 已完成 / 已发布
```

---

## AIHOT 采集说明

`ai-hotspots/fetch_aihot.py` 负责：
1. 调用 `aihot.virxact.com/api/public/daily` 获取每日 AI 热点（168 个信源）
2. 解析 JSON 数据，提取中文标题、摘要、来源、链接
3. 生成 `ai-hotspots/hotspots/AI热点-YYYY-MM-DD.md`（完整日报）
4. 更新 `今日热点速览.md`（速览版）
5. 触发 AI 更新 `index.md` 和相关索引页

定时任务：`AIHOT-热点采集`，每 3 天 08:00 自动运行。

---

## Obsidian 配置建议

1. **Vault 路径**: `D:\my_knowledgebase`
2. **启用核心插件**: 图谱视图、标签视图、大纲视图
3. **推荐社区插件**:
   - **Dataview**: 动态查询（如"列出本周所有 AI 热点"）
   - **Templater**: 快速创建新条目
   - **Calendar**: 时间线视图
   - **Web Clipper**: 一键保存网页为 Markdown
   - **Excalidraw**: 画架构图/流程图
4. **模板配置**: 将热点条目模板和笔记模板配置到 Templater

---

## 注意事项

1. **所有 AI 热点内容必须中文存储**（人名/专业名词保留英文并加注解）
2. **所有 AI 热点必须附带原始链接**
3. **所有 AI 热点必须有采集时间标签**
4. **逻辑冲突检测报告必须等待用户反馈后再处理**
5. **原始素材（`raw_sources/`）AI 只读不改**
6. **`index.md` 每次录入后必须更新**
7. **`log.md` 每次操作后必须追加记录**
