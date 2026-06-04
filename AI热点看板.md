---
title: "AI 热点看板"
created: 2026-06-03
tags: [dashboard, dataview]
---

# 📊 AI 热点看板

> 由 Dataview 自动聚合，无需手动更新。

---

## 🔥 今日热点速览（中文）

```dataview
LIST WITHOUT ID
  "**" + dateformat(file.cday, "yyyy-MM-dd") + "** | " + file.link
FROM "今日热点速览"
SORT file.cday DESC
LIMIT 1
```

👉 [查看最新中文热点标题](今日热点速览.md)

---

## 📰 最新热点文件（按日期倒序）

```dataview
TABLE without id
  file.link as "📰 文件",
  dateformat(file.cday, "yyyy-MM-dd") as "📅 日期",
  length(file.lists) as "📝 条目数"
FROM "ai-hotspots/hotspots"
SORT file.cday DESC
LIMIT 10
```

---

## 📈 热点统计

```dataview
TABLE without id
  length(rows) as "📊 文件数"
FROM "ai-hotspots/hotspots"
GROUP BY dateformat(file.cday, "yyyy-MM") as "📅 月份"
SORT key DESC
```

---

## 📅 按月份归档

```dataview
TABLE without id
  length(rows) as "📊 文件数",
  map(rows, (r) => r.file.link) as "📰 文件列表"
FROM "ai-hotspots/hotspots"
GROUP BY dateformat(file.cday, "yyyy-MM") as "📅 月份"
SORT key DESC
```

---

## 🔍 快速搜索

在 Obsidian 左侧搜索栏输入：
- `#security` → 查找安全相关热点
- `#vscode` → 查找 VSCode 相关热点
- `#llm` → 查找大语言模型相关热点
- `#ai-products` → 查找 AI 产品相关热点

---

> 💡 **使用提示**：
> - 点击文件名可打开详情
> - 点击 [今日热点速览](今日热点速览.md) 查看中文标题列表
> - 按 `Ctrl+P` 可快速搜索命令
> - 按 `Ctrl+O` 可快速打开文件
> - 按 `Ctrl+E` 切换编辑/预览模式
