# 🔄 标准操作流程 (SOP)

> **本文件定义所有 Agent 必须遵循的操作剧本。**

## 🎬 流程一：抖音视频 → 个人知识库

### 触发条件
- 用户输入包含 `v.douyin.com` 或 `douyin.com` 链接。
- 用户语义包含：“提取抖音”、“合入个人知识库”、“下载这个视频内容”。

### ⚠️ 强制规则
**每次用户给链接并要求合入个人知识库时，都必须尝试使用 `douyin-to-obsidian` skill 提取内容。**

---

### 操作步骤

#### 1. 识别与预处理
- **链接提取**：使用正则提取 `https://v.douyin.com/...` 或长链接。
- **环境校验**：
  - 检查 `py -3.10` 是否可用。
  - 检查 `ffmpeg` 是否在 PATH 中（Skill 依赖）。
- **Skill 调用**：**必须**指定使用 `douyin-to-obsidian` (路径：`D:\my_knowledgebase\tools\douyin-to-obsidian\`)。**禁止使用其他工具或手动下载。**

#### 2. 内容提取与修正
- **执行 Skill**：运行 `D:\my_knowledgebase\tools\douyin-to-obsidian\douyin_to_obsidian.py`。
- **加载修正规则**：读取 `D:\my_knowledgebase\tools\douyin-to-obsidian\text_corrections.json`。
- **自动替换**：对 Whisper 转录结果应用 JSON 中的映射规则（如"人设部"->"人社部"）。
- **人工校验**：将修正后的文本展示给用户，询问："错字修正结果是否正确？是否需要补充？"
- **等待确认**：**必须**等到用户确认后，才能执行写入操作。

#### 3. 文件命名与冲突检测
- **命名规则**：`抖音-视频标题前20字-作者.md`（例如：`抖音-公司要求学AI考证书指南-宁说宁话.md`）。
- **冲突检测**：
  - 检查 `D:\my_knowledgebase\personal\notes\` 下是否存在同名文件。
  - **如果冲突**：
    1. 提示用户："⚠️ 视频重复，知识库中已存在该内容：" + [展示旧内容]。
    2. 询问："是否覆盖更新？"
    3. **若用户同意**：读取旧文件，用新提取的内容**替换**原有内容（保留原文件元数据如创建时间）。
    4. **若用户拒绝**：停止操作，提示用户手动检查。

#### 4. 合入知识库
- **写入路径**：`D:\my_knowledgebase\personal\notes\`。
- **更新索引**：
  - 打开 `D:\my_knowledgebase\index.md`。
  - 在 `🧠 个人知识库` 表格中追加新行（或更新旧行）。
  - 更新统计信息（笔记总数 +1 或不变）。
- **更新日志**：
  - 在 `D:\my_knowledgebase\log.md` 中记录操作时间、链接、文件路径。

#### 5. 结果反馈
- 向用户展示：
  - 保存路径。
  - 索引更新状态。
  - 核心观点总结（从视频内容中提取）。

---

## 🔥 流程二：AI 热点采集 → AI-Hotspots

### 触发条件
- 用户语义包含：“采集AI热点”、“更新AI热点库”、“合入AI热点”。

### 操作步骤
1. 执行 `D:\my_knowledgebase\ai-hotspots\fetch_aihot.py`。
2. 验证输出：`D:\my_knowledgebase\ai-hotspots\hotspots\AI热点-日期.md`。
3. 更新 `index.md` 的 `🔥 AI 行业热点库` 段落。
4. 提示用户：“✅ AI 热点已更新。”

---

## 🚨 异常处理

### 场景 A：Skill 调用失败 (FFmpeg 错误)
- **现象**：`FileNotFoundError: ffmpeg`。
- **处理**：
  1. 提示用户：“⚠️ 缺少 FFmpeg，正在尝试自动修复...”
  2. 搜索 `imageio-ffmpeg` 的二进制路径。
  3. 将 `ffmpeg.exe` 路径写入 `config.py` 或添加到系统 PATH。

### 场景 B：链接失效
- **现象**：下载失败，返回 403 或 404。
- **处理**：提示用户：“⚠️ 抖音链接已失效，请重新生成分享链接。”

### 场景 C：转录质量极差
- **现象**：修正后依然大量乱码。
- **处理**：提示用户：“⚠️ 语音识别质量较低，建议手动校对或提供视频字幕文件。”
