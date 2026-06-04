#!/usr/bin/env python3
"""获取 AIHOT 日报并生成 Markdown 保存到知识库"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 aihot-skill/0.2.0"
HEADERS = {"User-Agent": UA, "Content-Type": "application/json"}
BASE_URL = "https://aihot.virxact.com"
OUT_DIR = r"D:\my_knowledgebase\ai-hotspots\hotspots"
SUMMARY_OUT = r"D:\my_knowledgebase\今日热点速览.md"

SECTION_NAMES = ["模型发布/更新", "产品发布/更新", "行业动态", "论文研究", "技巧与观点"]

def fetch_daily(date_str=None):
    url = f"{BASE_URL}/api/public/daily"
    if date_str:
        url = f"{BASE_URL}/api/public/daily/{date_str}"
    print(f"📡 请求: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()

def utc_to_cst(utc_str):
    """将 UTC ISO 时间转为北京时间可读格式"""
    if not utc_str:
        return ""
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        cst = dt.astimezone(CST)
        now = datetime.now(CST)
        delta = now - cst
        if delta.days == 0:
            return f"今天 {cst.strftime('%H:%M')}"
        elif delta.days == 1:
            return f"昨天 {cst.strftime('%H:%M')}"
        else:
            return cst.strftime("%m/%d %H:%M")
    except Exception:
        return utc_str

def build_markdown(data):
    lines = []
    date_str = data.get("date", datetime.now(CST).strftime("%Y-%m-%d"))
    lines.append(f"# AI 热点日报 {date_str}\n")
    lines.append(f"> 数据来源：[AIHOT](https://aihot.virxact.com) | 生成时间：{datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST\n")

    # 主编导语
    lead = data.get("lead") or {}
    if lead and lead.get("title"):
        lines.append(f"## 💬 主编导语\n")
        lines.append(f"**{lead['title']}**\n")
        for p in (lead.get("paragraphs") or []):
            lines.append(f"{p}\n")
        lines.append("")

    # 各版块
    sections = data.get("sections") or []
    global_idx = 1
    for i, sec in enumerate(sections):
        sec_name = SECTION_NAMES[i] if i < len(SECTION_NAMES) else f"版块{i+1}"
        items = sec.get("items") or []
        if not items:
            continue
        lines.append(f"## {global_idx}. {sec_name}（{len(items)} 条）\n")
        global_idx += 1
        for j, item in enumerate(items, 1):
            title = item.get("title") or item.get("title_en") or "（无标题）"
            summary = item.get("summary") or ""
            source = item.get("sourceName") or ""
            url = item.get("sourceUrl") or ""
            pub_at = utc_to_cst(item.get("publishedAt"))
            lines.append(f"### {j}. {title}\n")
            if pub_at:
                lines.append(f"🕐 {pub_at} | 📰 {source}\n")
            if summary:
                lines.append(f"{summary}\n")
            if url:
                lines.append(f"🔗 [阅读原文]({url})\n")
            lines.append("")

    return "\n".join(lines)

def build_summary(data):
    """生成今日热点速览（仅标题+摘要，轻量版）"""
    lines = []
    date_str = data.get("date", datetime.now(CST).strftime("%Y-%m-%d"))
    lines.append(f"# 📰 今日 AI 热点速览（{date_str}）\n")
    lines.append(f"> 数据来源：[AIHOT](https://aihot.virxact.com) | 更新：{datetime.now(CST).strftime('%Y-%m-%d %H:%M')} CST\n")

    lead = data.get("lead") or {}
    if lead and lead.get("title"):
        lines.append(f"## 💬 主编导语\n**{lead['title']}**\n")

    sections = data.get("sections") or []
    global_idx = 1
    for i, sec in enumerate(sections):
        items = sec.get("items") or []
        if not items:
            continue
        sec_name = SECTION_NAMES[i] if i < len(SECTION_NAMES) else f"版块{i+1}"
        lines.append(f"## {global_idx}. {sec_name}（{len(items)} 条）\n")
        global_idx += 1
        for j, item in enumerate(items, 1):
            title = item.get("title") or item.get("title_en") or "（无标题）"
            summary = item.get("summary") or "（暂无摘要）"
            url = item.get("sourceUrl") or ""
            source = item.get("sourceName") or ""
            lines.append(f"### {j}. {title}\n")
            lines.append(f"⭐ 来源：{source}\n")
            lines.append(f"{summary}\n")
            if url:
                lines.append(f"🔗 [阅读原文]({url})\n")
            lines.append("")

    return "\n".join(lines)

def save_summary(summary_text):
    os.makedirs(os.path.dirname(SUMMARY_OUT), exist_ok=True)
    with open(SUMMARY_OUT, "w", encoding="utf-8") as f:
        f.write(summary_text)
    print(f"✅ 速览已保存: {SUMMARY_OUT}")

def save_markdown(md_text, date_str):
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"AI热点-{date_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md_text)
    print(f"✅ 已保存: {path}")
    return path

def update_index(date_str):
    """更新 index.md，添加今日热点条目"""
    index_path = r"D:\my_knowledgebase\index.md"
    entry = f"- [{date_str} AI热点](ai-hotspots/hotspots/AI热点-{date_str}.md)"
    if not os.path.exists(index_path):
        print(f"⚠️  index.md 不存在，跳过更新")
        return
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    if date_str in content:
        print(f"ℹ️  index.md 已有 {date_str} 条目，跳过")
        return
    # 在 "近期热点（hotspots/）" 后插入
    marker = "### 近期热点（hotspots/）"
    if marker in content:
        new_content = content.replace(marker, marker + "\n" + entry)
    else:
        new_content = content + f"\n{entry}\n"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ index.md 已更新，添加 {date_str} 条目")

def main():
    import sys
    args = sys.argv[1:]
    only_summary = "--summary" in args or "-s" in args
    no_summary = "--no-summary" in args

    today = datetime.now(CST).strftime("%Y-%m-%d")
    data = fetch_daily(today)
    print(f"📦 日报日期: {data.get('date')}")
    total = sum(len((s or {}).get("items") or []) for s in (data.get("sections") or []))
    print(f"📊 总条目数: {total}")

    date_str = data.get("date", today)

    # 生成完整日报（默认生成，除非只生成速览）
    if not only_summary:
        md = build_markdown(data)
        path = save_markdown(md, date_str)
        update_index(date_str)
        print(f"✅ 完整日报已保存: {path}")

    # 生成速览（默认生成，除非 --no-summary）
    if not no_summary:
        summary = build_summary(data)
        save_summary(summary)
        print(f"✅ 今日热点速览已更新: {SUMMARY_OUT}")

    print(f"\n🎉 完成！")

if __name__ == "__main__":
    main()
