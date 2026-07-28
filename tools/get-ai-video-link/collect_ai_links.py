from __future__ import annotations

import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path

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
    t = (item.get("desc") or item.get("title") or "")
    t = t.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    t = re.sub(r"[\x00-\x1f\x7f]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > 120:
        t = t[:117] + "..."
    return t


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


async def collect_new(session, max_items=MAX_ITEMS):
    if session._page is None:
        raise RuntimeError("Browser not open")

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
        "title: douyin-ai-favorites",
        f"date: {today}",
        "---",
        "",
        f"# Ai favorites ({len(all_items)} items)",
        "",
        f"> Updated: {today}",
        f"> New this run: {new_count}",
        "",
        "---",
        "",
    ]
    for item in all_items:
        t = _title(item)
        idx = item["index"]
        aid = item["aweme_id"]
        lines.append(f"{idx}. **{t}** @{item['author']}")
        lines.append(f"   URL: https://www.douyin.com/video/{aid}")
        lines.append("")

    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    return {"total": len(all_items), "new": new_count, "json": str(JSON_PATH), "md": str(MD_PATH)}


async def _run(max_items=MAX_ITEMS):
    print(f"[get-ai-video-link] collecting up to {max_items} items...")

    existing_map, _ = load_existing()
    print(f"[get-ai-video-link] existing: {len(existing_map)} items")

    profile_override = Path(BROWSER_PROFILE_DIR) if BROWSER_PROFILE_DIR else None
    if profile_override:
        session = BrowserSession(profile_dir=profile_override, channel=None)
        await session.open(headless=True)
        await session.navigate()
        if not await session.authenticated():
            await session.close()
            raise RuntimeError("Profile not authenticated")
    else:
        session = await ensure_authenticated(channel=None)

    try:
        new_items = await collect_new(session, max_items=max_items)
        print(f"[get-ai-video-link] fetched: {len(new_items)} items")

        added = 0
        for item in new_items:
            aid = item["aweme_id"]
            if aid not in existing_map:
                title_clean = _title(item)
                existing_map[aid] = {
                    "index": 0,
                    "aweme_id": aid,
                    "title": title_clean,
                    "author": item.get("author", ""),
                    "url": f"https://www.douyin.com/video/{aid}",
                }
                added += 1
                print(f"  [NEW] #{len(existing_map)}: {title_clean[:60]} | @{item.get('author', '')}")

        all_items = list(existing_map.values())
        result = save_outputs(all_items, added)

        print(f"\n[get-ai-video-link] done! total={result['total']}, new={result['new']}")
        print(f"  JSON: {result['json']}")
        print(f"  MD:   {result['md']}")
        print("\n__RESULT__")
        print(json.dumps(result, ensure_ascii=False))
    finally:
        await session.close()


def main():
    max_items = MAX_ITEMS
    do_login = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--max="):
            max_items = int(arg.split("=", 1)[1])
        elif arg == "--max" and i + 1 < len(args):
            i += 1
            max_items = int(args[i])
        elif arg == "--login":
            do_login = True
        i += 1

    if do_login:
        from browser_login import login as do_login_func
        result = do_login_func()
        print(json.dumps(result, ensure_ascii=False))
        if result.get("status") != "ok":
            return 1

    asyncio.run(_run(max_items=max_items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())