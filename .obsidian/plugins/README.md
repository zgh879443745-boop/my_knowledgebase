# Obsidian 插件配置说明

## 必须安装的社区插件

1. **Templater**
   - 用途：使用模板快速创建新条目
   - 配置：将模板目录设置为 `.obsidian/templates/`

2. **Dataview**
   - 用途：动态查询知识库内容（如"列出本周所有 AI 热点"）
   - 示例查询：
     ```dataview
     TABLE 采集时间, 热度评分, 状态
     FROM "ai-hotspots/hotspots"
     WHERE 采集时间 >= date(today) - dur(7 days)
     SORT 采集时间 DESC
     ```

3. **Calendar**
   - 用途：时间线视图，按日期查看热点

4. **Web Clipper**
   - 用途：一键保存网页为 Markdown 到 `raw_sources/`

5. **Excalidraw**
   - 用途：画架构图/流程图

## 核心插件（默认启用）

- 图谱视图（Graph View）
- 标签视图（Tag View）
- 大纲视图（Outline View）
- 页面预览（Page Preview）

## Templater 配置示例

在 Templater 设置中：
- Template Folder Location: `.obsidian/templates`
- Trigger Templater on new file creation: `true`

## Dataview 查询示例

### 查询本周 AI 热点
```dataview
TABLE 热度评分, 状态
FROM "ai-hotspots/hotspots"
WHERE file.ctime >= date(today) - dur(7 days)
SORT 热度评分 DESC
```

### 查询所有标签统计
```dataview
TABLE length(file.tags) as "标签数"
FROM ""
WHERE file.tags
SORT length(file.tags) DESC
```

### 查询个人笔记
```dataview
TABLE 状态
FROM "personal/notes"
SORT file.mtime DESC
```
