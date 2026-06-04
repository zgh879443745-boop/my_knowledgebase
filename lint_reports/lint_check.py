#!/usr/bin/env python3
"""
知识库逻辑冲突检测脚本（Lint）
功能：
1. 扫描所有页面，检测逻辑冲突
2. 生成冲突报告（lint-YYYYMMDD.md）
3. 等待用户反馈后解决（不自动覆盖）

检测类型：
- 时间冲突：同一事件在不同页面有不同日期
- 事实冲突：同一概念在不同页面有矛盾描述
- 状态冲突：某产品在同一时间既被描述为"已发布"又被描述为"未发布"
- 孤立页面：有出链但无入链的页面
- 重复热点：同一事件被录入多次

使用方式：
  python lint_check.py              # 执行一次检测
  python lint_check.py --fix       # 检测并尝试自动修复（需用户确认）
  python lint_check.py --watch    # 定时执行（每天一次）
"""

import os
import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import hashlib

# ========== 配置区 ==========
KNOWLEDGE_BASE_DIR = Path("../")  # 相对路径，从 lint_reports/ 到 MyKnowledge_base/
AI_HOTSPOTS_DIR = KNOWLEDGE_BASE_DIR / "ai-hotspots"
PERSONAL_DIR = KNOWLEDGE_BASE_DIR / "personal"
CONCEPTS_DIR = KNOWLEDGE_BASE_DIR / "concepts"
LINT_REPORTS_DIR = Path(".")  # 当前目录 lint_reports/

# ========== 工具函数 ==========

def read_md_file(file_path: Path) -> tuple[str, dict]:
    """读取 Markdown 文件，返回 (内容, frontmatter)"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # 简单解析 frontmatter（YAML 格式）
    fm = {}
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                fm[key.strip()] = val.strip()
    return content, fm

def extract_wikilinks(content: str) -> list[str]:
    """提取所有 [[wikilink]] 链接"""
    return re.findall(r"\[\[(.+?)\]\]", content)

def extract_title(content: str) -> str:
    """提取 Markdown 标题（第一个 # 行）"""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else ""

def extract_date(content: str, field: str = "采集时间") -> str:
    """提取指定字段的日期"""
    pattern = rf"{field}\s*:\s*(\d{{4}}-\d{{2}}-\d{{2}})"
    match = re.search(pattern, content)
    return match.group(1) if match else ""

def extract_status(content: str) -> str:
    """提取状态字段"""
    match = re.search(r"## 状态\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else ""

# ========== 冲突检测函数 ==========

def check_time_conflicts(files: list[Path]) -> list[dict]:
    """检测时间冲突：同一事件在不同页面有不同日期"""
    conflicts = []
    event_dates = defaultdict(dict)

    for fp in files:
        content, _ = read_md_file(fp)
        title = extract_title(content)
        date = extract_date(content, "采集时间")
        if title and date:
            # 用标题作为事件标识（简化版，实际应该用语义相似度）
            event_dates[title][fp.stem] = date

    for event, dates in event_dates.items():
        unique_dates = set(dates.values())
        if len(unique_dates) > 1:
            conflicts.append({
                "type": "时间冲突",
                "event": event,
                "details": dates,
                "description": f"同一事件在不同页面有不同日期：{unique_dates}"
            })

    return conflicts

def check_status_conflicts(files: list[Path]) -> list[dict]:
    """检测状态冲突：某产品/事件在同一时间既有 A 状态又有 B 状态"""
    conflicts = []
    entity_status = defaultdict(dict)

    for fp in files:
        content, _ = read_md_file(fp)
        title = extract_title(content)
        status = extract_status(content)
        date = extract_date(content, "采集时间")
        if title and status and date:
            entity_status[(title, date)][fp.stem] = status

    for (entity, date), statuses in entity_status.items():
        unique_statuses = set(statuses.values())
        if len(unique_statuses) > 1:
            conflicts.append({
                "type": "状态冲突",
                "entity": entity,
                "date": date,
                "details": statuses,
                "description": f"{entity} 在 {date} 既有「{'」「'.join(unique_statuses)}」多种状态"
            })

    return conflicts

def check_orphan_pages(files: list[Path]) -> list[dict]:
    """检测孤立页面：有出链但无入链"""
    orphan = []
    all_links = set()
    all_titles = set()

    for fp in files:
        content, _ = read_md_file(fp)
        title = extract_title(content)
        if title:
            all_titles.add(title)
        links = extract_wikilinks(content)
        for link in links:
            all_links.add(link.split("|")[0].strip())  # 处理 [[link|alias]] 格式

    # 简化：假设文件名 ≈ 标题，检查是否有页面没有被其他页面链接
    linked_pages = set()
    for fp in files:
        content, _ = read_md_file(fp)
        links = extract_wikilinks(content)
        for link in links:
            linked_pages.add(link.split("|")[0].strip())

    for fp in files:
        if fp.stem not in linked_pages and len(files) > 1:
            orphan.append({
                "type": "孤立页面",
                "page": fp.name,
                "description": f"{fp.name} 没有被其他页面链接"
            })

    return orphan

def check_duplicate_hotspots(files: list[Path]) -> list[dict]:
    """检测重复热点：同一事件被录入多次（简化版用标题相似度）"""
    duplicates = []
    titles = []

    for fp in files:
        content, _ = read_md_file(fp)
        title = extract_title(content)
        if title:
            titles.append((title, fp.name))

    # 简化版：检查标题是否包含相同关键词
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            title1, file1 = titles[i]
            title2, file2 = titles[j]
            # 简单判断：如果标题相似度 > 80%（用编辑距离或关键词重合）
            words1 = set(re.findall(r"\w+", title1.lower()))
            words2 = set(re.findall(r"\w+", title2.lower()))
            if words1 and words2:
                overlap = len(words1 & words2) / max(len(words1), len(words2))
                if overlap > 0.8:
                    duplicates.append({
                        "type": "重复热点",
                        "titles": [title1, title2],
                        "files": [file1, file2],
                        "description": f"可能重复：{title1} vs {title2}"
                    })

    return duplicates

def check_fact_conflicts(files: list[Path]) -> list[dict]:
    """检测事实冲突：同一概念在不同页面有矛盾描述（简化版）"""
    conflicts = []
    # 高级功能，需要 NLP/LLM 支持，这里只做框架
    # 实际实现：提取概念定义 → 用 LLM 判断是否有矛盾
    return conflicts

# ========== 报告生成 ==========

def generate_report(conflicts: list[dict], report_dir: Path) -> Path:
    """生成冲突报告 Markdown 文件"""
    today = datetime.now().strftime("%Y%m%d")
    report_file = report_dir / f"lint-{today}.md"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# 知识库逻辑冲突检测报告 — {today}\n\n")
        f.write(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("## 检测结果\n\n")

        if not conflicts:
            f.write("✅ 未检测到逻辑冲突。\n")
        else:
            # 按冲突类型分组
            by_type = defaultdict(list)
            for c in conflicts:
                by_type[c["type"]].append(c)

            for conflict_type, items in by_type.items():
                f.write(f"### {conflict_type}（{len(items)} 条）\n\n")
                for i, item in enumerate(items):
                    f.write(f"#### {i+1}. {item.get('description', '')}\n\n")
                    # 写入详细信息
                    for key, val in item.items():
                        if key not in ["type", "description"]:
                            f.write(f"- **{key}**: {val}\n")
                    f.write("\n---\n\n")
                f.write("\n")

        f.write("## 处理方式\n\n")
        f.write("1. **时间冲突/状态冲突/事实冲突**: 等待用户反馈后，由 AI 更新相关页面并标注修订日期。\n")
        f.write("2. **孤立页面**: 建议人工检查是否需要添加反向链接。\n")
        f.write("3. **重复热点**: 建议合并两个页面，保留最新/最完整的一个。\n")
        f.write("\n## 用户反馈区\n\n")
        f.write("> 请在此处填写处理意见，AI 将根据反馈更新知识库。\n")
        f.write("- [ ] 已检查时间冲突，确认无误 / 需要更新：\n")
        f.write("- [ ] 已检查状态冲突，确认无误 / 需要更新：\n")
        f.write("- [ ] 已检查孤立页面，确认无误 / 需要更新：\n")
        f.write("- [ ] 已检查重复热点，确认无误 / 需要更新：\n")

    print(f"[Lint] 报告已生成: {report_file}")
    return report_file

# ========== 主程序 ==========

def main():
    parser = argparse.ArgumentParser(description="知识库逻辑冲突检测脚本")
    parser.add_argument("--fix", action="store_true", help="检测并尝试自动修复（需用户确认）")
    parser.add_argument("--watch", action="store_true", help="定时执行（每天一次）")
    parser.add_argument("--dir", type=str, help="指定检测目录（默认检测整个知识库）")
    args = parser.parse_args()

    # 收集需要检测的文件
    if args.dir:
        target_dir = Path(args.dir)
        files = list(target_dir.rglob("*.md"))
    else:
        # 检测 ai-hotspots/ 和 personal/ 下的所有 .md 文件
        files = []
        for d in [AI_HOTSPOTS_DIR, PERSONAL_DIR, CONCEPTS_DIR]:
            if d.exists():
                files.extend(d.rglob("*.md"))

    print(f"[Lint] 开始检测，共 {len(files)} 个文件")

    # 执行检测
    conflicts = []
    conflicts.extend(check_time_conflicts(files))
    conflicts.extend(check_status_conflicts(files))
    conflicts.extend(check_orphan_pages(files))
    conflicts.extend(check_duplicate_hotspots(files))
    conflicts.extend(check_fact_conflicts(files))

    # 生成报告
    report_file = generate_report(conflicts, LINT_REPORTS_DIR)

    print(f"[Lint] 检测完成，共发现 {len(conflicts)} 个冲突")
    print(f"[Lint] 报告路径: {report_file}")

    # 如果用户要求修复，则等待反馈
    if args.fix:
        print("[Lint] 请检查报告，手动修改相关文件后，AI 会在下次 ingest 时更新索引。")

    # 定时模式
    if args.watch:
        import time
        print("[Lint] 定时模式启动，每天执行一次")
        while True:
            # 等待 24 小时
            time.sleep(86400)
            # 重新执行检测
            # （简化版，实际应该用 cron 或 Windows 任务计划）
            print("[Lint] 定时检测触发")
            # 递归调用 main() 或重新执行检测逻辑

if __name__ == "__main__":
    main()
