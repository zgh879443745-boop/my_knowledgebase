# 🧠 AI Blogger 知识库

> 基于 Karpathy LLM Wiki Pattern 构建的双库知识管理系统  
> AI Agent 自动维护 · 人类 Obsidian 浏览 · Git 版本控制

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 🎬 抖音视频 → 结构化笔记 | Whisper 语音识别 → 错字修正 → AI 提炼摘要/观点 |
| 🔥 AI 热点自动采集 | 定时抓取行业资讯，生成中文简报 |
| 📝 快速文字笔记 | 口述/粘贴即保存，AI 按模板整理 |
| 🤖 Agent 开箱即用 | `AGENTS.md` 自动加载，任何 AI Agent 接入即知规则 |

---

## 📂 双库架构

```
MyKnowledge_base/
├── AGENTS.md            ← Agent 入职指南（自动加载）
├── SCHEMA.md            ← 知识库结构与规则
├── WORKFLOW.md          ← 标准操作流程 (SOP)
├── index.md             ← 总索引
├── log.md               ← 操作日志
│
├── personal/            ← 🧠 个人知识库
│   └── notes/           ← 笔记（支持子文件夹分类）
│       ├── codex_notes/ ← Codex 专题
│       ├── 抖音-LLM Wiki 和 GBrain 真正的差别.md
│       ├── 抖音-公司要求学AI考证书指南.md
│       └── 抖音-让Codex干活飞起.md
│
├── ai-hotspots/         ← 🔥 AI 行业热点库
│   ├── hotspots/        ← 每日热点条目
│   ├── concepts/        ← 概念解释页
│   ├── people/          ← 人物索引
│   ├── companies/       ← 公司/产品索引
│   └── daily/           ← 每日简报归档
│
├── tools/               ← 🛠️ 工具集
│   └── douyin-to-obsidian/  ← 抖音视频提取 Skill
│
├── concepts/            ← 跨库共享概念
├── timeline/            ← 时间线视图
└── lint_reports/        ← 逻辑冲突检测
```

---

## 🎬 一条抖音链接的工作流

```
抖音链接 → 判断目标库（个人/AI热点）
  → douyin_to_obsidian.py 下载视频
  → Whisper 本地语音识别（中文优化）
  → text_corrections.json 自动修正错字
  → AI 提炼摘要 + 核心观点 + 关键笔记
  → 用户确认 → 按模板写入
  → 更新 index.md + log.md
  → Git 提交 → GitHub 同步
```

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 知识管理 | Obsidian |
| 语音识别 | OpenAI Whisper (local) |
| 视频处理 | FFmpeg + MoviePy |
| 版本控制 | Git + GitHub |
| AI Agent | Codex CLI / 任意兼容 Agent |
| 规则体系 | AGENTS.md + SCHEMA.md + WORKFLOW.md |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- FFmpeg
- Obsidian（可选，用于可视化浏览）
- Git

### 安装依赖

```bash
pip install requests openai-whisper moviepy imageio-ffmpeg ffmpeg-python
```

### 使用

**方式一：AI Agent 对话（推荐）**

```
"帮我把这个抖音视频合入知识库：https://v.douyin.com/xxxxx"
"采集今天的 AI 热点"
"帮我把这段文字记到知识库：..."
```

**方式二：命令行**

```bash
# 提取抖音视频到个人知识库
py -3.10 tools/douyin-to-obsidian/douyin_to_obsidian.py --link "链接" --target personal

# 提取抖音视频到 AI 热点库
py -3.10 tools/douyin-to-obsidian/douyin_to_obsidian.py --link "链接" --target aihot
```

---

## 🤖 Agent 接入

任何兼容 AGENTS.md 规范的 AI Agent 接入后会自动：
- 读取知识库规则体系
- 识别用户意图并路由到正确知识库
- 按 SOP 执行内容提取与写入
- 维护索引和操作日志

详见 [`AGENTS.md`](AGENTS.md)。

---

## 📊 当前状态

| 类别 | 条目数 |
|------|--------|
| 个人笔记 | 3 |
| AI 热点 | 4 天 |
| 博文草稿 | 0 |
| 选题想法 | 0 |

---

## 📄 License

MIT
