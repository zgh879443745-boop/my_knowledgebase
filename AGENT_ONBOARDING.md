# 🤖 Agent 入职指南

> **本文件是新 Agent 的必读手册，必须在首次处理用户请求前阅读本文档。**

## 🎯 核心职责

1. **抖音视频处理**：使用 `douyin-to-obsidian` skill 提取内容并合入 `personal` 知识库。
2. **AI 热点采集**：定时或按需采集 AI 行业资讯合入 `ai-hotspots` 知识库。
3. **规则严守**：严格按照 `SCHEMA.md` 和 `WORKFLOW.md` 定义的规则执行，不得跳步。

---

## 🚀 启动检查清单 (Checklist)

在新 Agent 开始工作前，必须确认以下环境配置：

### 1. 环境依赖
- [ ] **Python 版本**：必须 >= 3.10 (Whisper 依赖)。
  - 验证命令：`py -3.10 --version`
- [ ] **FFmpeg**：必须安装并配置环境变量，或配置在 `config.py` 中。
  - 验证命令：`ffmpeg -version`
- [ ] **必要 Python 包**：`requests`, `openai-whisper`, `moviepy`, `imageio-ffmpeg`, `ffmpeg-python`。
  - 安装命令：`py -3.10 -m pip install -r requirements.txt`

### 2. 路径配置
- [ ] **知识库根目录**：`D:\my_knowledgebase`
- [ ] **Skill 目录**：`D:\my_knowledgebase\tools\douyin-to-obsidian\`
- [ ] **输出目录**：
  - 个人库：`D:\my_knowledgebase\personal\notes\`
  - 热点库：`D:\my_knowledgebase\ai-hotspots\hotspots\`

### 3. 规则文件读取
- [ ] 阅读 `SCHEMA.md` (Schema 与双库规则)
- [ ] 阅读 `WORKFLOW.md` (详细操作流程)
- [ ] 检查 `text_corrections.json` (错字修正规则)

---

## 📚 必读文件顺序

请严格按照以下顺序阅读，以理解项目全貌：

1. **`SCHEMA.md`** - 理解知识库结构、双库语义映射规则。
2. **`WORKFLOW.md`** - 掌握抖音视频处理的 Standard Operating Procedure (SOP)。
3. **`text_corrections.json`** - 了解常见错字映射，提高转录质量。
4. **`log.md`** - 查看历史操作记录，了解上下文。

---

## ⚠️ 高危禁止操作 (DON'Ts)

1. **严禁混淆库**：
   - 抖音个人内容 **禁止** 写入 `ai-hotspots`。
   - AI 行业资讯 **禁止** 写入 `personal`。
2. **严禁跳过修正**：
   - 使用 `douyin-to-obsidian` 提取后，**必须**应用 `text_corrections.json` 进行错字修正。
3. **严禁无确认覆盖**：
   - 遇到文件命名冲突，**必须**提示用户并展示重复内容，不得直接覆盖。

---

## 🛠️ 故障排查

### Skill 调用失败
- 检查 Python 版本是否为 3.10。
- 检查 `config.py` 中的 `OBSIDIAN_PATH` 是否指向 `D:\my_knowledgebase`。

### 转录内容乱码/错字多
- 检查 `text_corrections.json` 是否包含该视频领域（如IT认证、农业）的专有名词修正。
- 若规则缺失，提示用户更新 `text_corrections.json`。

### 文件路径错误
- 确认 Windows 路径使用双反斜杠 `\\` 或原始字符串 `r"..."`。
