# -*- coding: utf-8 -*-
"""collect_ai_links.py - \u4ece\u6296\u97f3\u6536\u85cf\u5939\u300cAi\u300d\u63d0\u53d6\u89c6\u9891\u94fe\u63a5

\u589e\u91cf\u66f4\u65b0\u3001\u53bb\u91cd\u9632\u91cd\u3002\u9996\u6b21\u8fd0\u884c\u521b\u5efa\u6587\u6863\uff0c\u540e\u7eed\u8fd0\u884c\u4ec5\u8ffd\u52a0\u65b0\u89c6\u9891\u3002

\u7528\u6cd5:
    python collect_ai_links.py            # \u9ed8\u8ba4\u91c7\u96c6 100 \u6761
    python collect_ai_links.py --max 200  # \u6307\u5b9a\u6570\u91cf
    python collect_ai_links.py --login    # \u5148\u767b\u5f55\u518d\u91c7\u96c6
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import date
from pathlib import Path

# \u5c1d\u8bd5\u52a0\u8f7d\u914d\u7f6e
try:
    from config import COLLECTS_ID, OUTPUT_DIR, BROWSER_PROFILE_DIR, MAX_ITEMS, PAGE_SIZE, FETCH_DELAY
except ImportError:
    COLLECTS_ID = "7610341807192299291"
    OUTPUT_DIR = Path("D:/my_knowledgebase/personal/notes")
    BROWSER_PROFILE_DIR = None
    MAX_ITEMS = 100
    PAGE_SIZE = 20
    FETCH_DELAY = 0.5

from browser_login import BrowserSession, ensure_authenticated

API_URL = "https://www.douyin.com/aweme/v1/web/collects/video/list/"
OUTPUT_DIR = Path(OUTPUT_DIR)
JSON_PATH = OUTPUT_DIR / "douyin-ai-favorites-links.json"
MD_PATH = OUTPUT_DIR / "douyin-ai-favorites.md"


def _title(item: dict) -> str:
    return (item.get("desc") or item.get("title") or "").replace("\n", " ").replace("\r", "").strip()


def load_existing():
    if not JSON_PATH.exists():
        return {}, []
    try:
        items = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        mapping = {}
        for item in items:
            aid = item.get("aweme_id", "")
            if aid:
                mapping[aid] = {
                    "index": item.get("index", 0),
                    "aweme_id": aid,
                    "title": _title(item),
                    "author": item.get("author", ""),
                    "url": item.get("url", f"https://www.douyin.com/video/{aid}"),
                }
        return mapping, list(mapping.values())
    except Exception:
        return {}, []


async def collect_new(session: BrowserSession, max_items: int = MAX_ITEMS):
    if session._page is None:
        raise RuntimeError("\u6d4f\u89c8\u5668\u672a\u6253\u5f00")

    collected = {}
    cursor = 0
    seen_cursors = set()

    while len(collected) < max_items:
        count = min(PAGE_SIZE, max_items - len(collected) + 5)

        result = await session._page.evaluate(
            """async ({apiUrl, collectsId, cursor, count}) => {
                var params = new URLSearchParams({
                    device_platform: "webapp", aid: "6383",
                    channel: "channel_pc_web", collects_id: collectsId,
                    cursor: String(cursor), count: String(count),
                    cookie_enabled: String(navigator.cookieEnabled),
                    browser_language: navigator.language || "zh-CN",
                    browser_platform: navigator.platform || "",
                    browser_name: "Chrome",
                });
                var r = await fetch(apiUrl + "?" + params.toString(), {credentials: "include"});
                var data = await r.json();
                return {
                    ok: data.status_code === 0,
                    status_code: data.status_code,
                    cursor: Number(data.cursor || 0),
                    has_more: Boolean(data.has_more),
                    items: (data.aweme_list || []).map(function(item) {
                        return {
                            aweme_id: String(item.aweme_id || ""),
                            desc: (item.desc || "").split("\\n")[0].trim(),
                            author: item.author ? (item.author.nickname || "") : "",
                        };
                    }),
                };
            }""",
            {"apiUrl": API_URL, "collectsId": COLLECTS_ID, "cursor": cursor, "count": count},
        )

        if not result["ok"]:
            print(f"[ERROR] API status_code={result['status_code']}", file=sys.stderr)
            break

        for item in result["items"]:
            aid = item.get("aweme_id", "")
            if aid and aid not in collected:
                collected[aid] = item

        if not result.get("has_more") or not result.get("items"):
            break

        next_cursor = result.get("cursor", 0)
        if next_cursor in seen_cursors or next_cursor == cursor:
            break
        seen_cursors.add(cursor)
        cursor = next_cursor
        await asyncio.sleep(FETCH_DELAY)

    return list(collected.values())[:max_items]


def save_outputs(all_items, new_count):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, item in enumerate(all_items, 1):
        item["index"] = i
        if "title" not in item:
            item["title"] = _title(item)

    JSON_PATH.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")

    today = date.today().isoformat()
    lines = [
        "---",
        "title: \u6296\u97f3\u6536\u85cf\u5939Ai-\u89c6\u9891\u94fe\u63a5\u5217\u8868",
        "tags: [\u6296\u97f3, \u6536\u85cf\u5939, Ai, \u89c6\u9891\u94fe\u63a5]",
        "source: \u6296\u97f3\u6536\u85cf\u5939",
        f"date: {today}",
        "author: \u7cfb\u7edf\u91c7\u96c6\uff08get-ai-video-link\uff09",
        "---",
        "",
        "# \u6296\u97f3\u6536\u85cf\u5939\u300cAi\u300d- \u89c6\u9891\u94fe\u63a5\u5217\u8868",
        "",
        f"> \u6700\u540e\u66f4\u65b0\uff1a{today}",
        f"> \u91c7\u96c6\u6765\u6e90\uff1a\u6296\u97f3\u6536\u85cf\u5939\u300cAi\u300d\uff08collects_id: {COLLECTS_ID}\uff09",
        f"> \u89c6\u9891\u6570\u91cf\uff1a{len(all_items)} \u6761\uff08\u5df2\u53bb\u91cd\uff09",
        f"> \u672c\u6b21\u65b0\u589e\uff1a{new_count} \u6761",
        f"> \u8bf4\u660e\uff1a\u6bcf\u6761\u94fe\u63a5\u683c\u5f0f\u4e3a https://www.douyin.com/video/{{aweme_id}}\uff0c\u53ef\u76f4\u63a5\u63d0\u4f9b\u7ed9 douyin-to-obsidian skill \u89e3\u6790",
        "",
        "---",
        "",
        "## \u94fe\u63a5\u5217\u8868",
        "",
    ]
    for item in all_items:
        t = _title(item)
        idx = item["index"]
        aid = item["aweme_id"]
        lines.append(f"{idx}. **{t}** \u2014 @{item['author']}")
        lines.append(f"   - URL: `https://www.douyin.com/video/{aid}`")
        lines.append(f"   - aweme_id: `{aid}`")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## \u7edf\u8ba1",
        "",
        f"- \u603b\u6570\uff1a{len(all_items)} \u6761",
        f"- \u672c\u6b21\u65b0\u589e\uff1a{new_count} \u6761",
        f"- \u53bb\u91cd\u65b9\u5f0f\uff1a\u6309 aweme_id \u5168\u5c40\u53bb\u91cd",
        f"- \u94fe\u63a5\u683c\u5f0f\uff1ahttps://www.douyin.com/video/{{aweme_id}}",
    ])
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")

    return {"total": len(all_items), "new": new_count, "json": str(JSON_PATH), "md": str(MD_PATH)}


async def _run(max_items: int = MAX_ITEMS):
    print(f"[get-ai-video-link] \u91c7\u96c6\u4e2d\uff0c\u76ee\u6807\u6700\u591a {max_items} \u6761...")

    existing_map, _ = load_existing()
    print(f"[get-ai-video-link] \u5df2\u6709\u6570\u636e\uff1a{len(existing_map)} \u6761")

    profile_override = Path(BROWSER_PROFILE_DIR) if BROWSER_PROFILE_DIR else None
    session = await ensure_authenticated(channel=None)
    if profile_override:
        await session.close()
        session = BrowserSession(profile_dir=profile_override)
        await session.open(headless=True)
        await session.navigate()
        if not await session.authenticated():
            await session.close()
            raise RuntimeError("\u6307\u5b9a profile \u76ee\u5f55\u672a\u767b\u5f55\uff0c\u8bf7\u68c0\u67e5\u914d\u7f6e")

    try:
        new_items = await collect_new(session, max_items=max_items)
        print(f"[get-ai-video-link] \u672c\u6b21\u91c7\u96c6\uff1a{len(new_items)} \u6761")

        added = 0
        for item in new_items:
            aid = item["aweme_id"]
            if aid not in existing_map:
                existing_map[aid] = {
                    "index": 0,
                    "aweme_id": aid,
                    "title": _title(item),
                    "author": item.get("author", ""),
                    "url": f"https://www.douyin.com/video/{aid}",
                }
                added += 1
                print(f"  [NEW] #{len(existing_map)}: {_title(item)[:60]} | @{item.get('author', '')}")

        all_items = list(existing_map.values())
        result = save_outputs(all_items, added)

        print(f"\n[get-ai-video-link] \u5b8c\u6210\uff01\u603b\u6570: {result['total']} \u6761, \u672c\u6b21\u65b0\u589e: {result['new']} \u6761")
        print(f"  JSON: {result['json']}")
        print(f"  MD:   {result['md']}")
        print("\n__RESULT__")
        print(json.dumps(result, ensure_ascii=False))
    finally:
        await session.close()


def main():
    max_items = MAX_ITEMS
    do_login = False

    for arg in sys.argv[1:]:
        if arg.startswith("--max="):
            max_items = int(arg.split("=", 1)[1])
        elif arg == "--max" and len(sys.argv) > sys.argv.index(arg) + 1:
            max_items = int(sys.argv[sys.argv.index(arg) + 1])
        elif arg == "--login":
            do_login = True

    if do_login:
        from browser_login import login as do_login_func
        result = do_login_func()
        print(json.dumps(result, ensure_ascii=False))
        if result.get("status") != "ok":
            return 1
        # \u767b\u5f55\u6210\u529f\u540e\u7ee7\u7eed\u91c7\u96c6
        print()

    asyncio.run(_run(max_items=max_items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
