# -*- coding: utf-8 -*-
"""browser_login.py - \u62b6\u97f3\u6d4f\u89c8\u5668\u767b\u5f55\u6a21\u5757

\u63d0\u4f9b\u767b\u5f55\u3001\u72b6\u6001\u68c0\u67e5\u3001\u767b\u51fa\u529f\u80fd\uff0c\u4f7f\u7528 Playwright \u6301\u4e45\u5316 Chromium context \u7ef4\u62a4\u767b\u5f55\u6001\u3002
\u53ef\u5355\u72ec\u4f7f\u7528\u6216\u4f5c\u4e3a\u6a21\u5757\u88ab\u5176\u4ed6\u811a\u672c\u5f15\u5165\u3002

\u7528\u6cd5:
    python browser_login.py login      # \u6253\u5f00\u6d4f\u89c8\u5668\u767b\u5f55
    python browser_login.py status     # \u68c0\u67e5\u767b\u5f55\u72b6\u6001
    python browser_login.py logout     # \u6e05\u9664\u767b\u5f55\u6001
"""

from __future__ import annotations

import asyncio
import os
import platform
import sys
from pathlib import Path
from typing import Any

# \u9ed8\u8ba4 profile \u76ee\u5f55\uff0c\u53ef\u901a\u8fc7\u73af\u5883\u53d8\u91cf DOUYIN_PROFILE_DIR \u8986\u76d6
def default_profile_dir() -> Path:
    override = os.environ.get("DOUYIN_PROFILE_DIR")
    if override:
        return Path(override).expanduser().resolve()
    system = platform.system()
    if system == "Darwin":
        root = Path.home() / "Library" / "Application Support"
    elif system == "Windows":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        root = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return root / "get-ai-video-link" / "browser-profile"


COLLECTION_PAGE_URL = "https://www.douyin.com/user/self?showTab=favorite_collection"
API_URL = "https://www.douyin.com/aweme/v1/web/aweme/listcollection/"
SESSION_COOKIE_NAMES = frozenset({"sessionid", "sessionid_ss", "sid_guard"})


class BrowserSession:
    """\u6d4f\u89c8\u5668\u4f1a\u8bdd\u7ba1\u7406\uff0c\u5c01\u88c5 Playwright \u6301\u4e45\u5316 context"""

    def __init__(self, profile_dir: Path | None = None, channel: str | None = None):
        self.profile_dir = (profile_dir or default_profile_dir()).expanduser().resolve()
        self.channel = channel
        self._playwright = None
        self._context = None
        self._page = None

    async def open(self, *, headless: bool) -> None:
        try:
            from playwright.async_api import async_playwright
        except ImportError as exc:
            raise RuntimeError(
                "Playwright \u672a\u5b89\u88c5\uff0c\u8bf7\u8fd0\u884c: pip install playwright && playwright install chromium"
            ) from exc

        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self._playwright = await async_playwright().start()

        channels = [self.channel] if self.channel else ["chrome", "msedge", None]
        for ch in channels:
            kwargs: dict[str, Any] = {
                "user_data_dir": str(self.profile_dir),
                "headless": headless,
                "viewport": {"width": 1280, "height": 800},
                "locale": "zh-CN",
            }
            if ch:
                kwargs["channel"] = ch
            try:
                self._context = await self._playwright.chromium.launch_persistent_context(**kwargs)
                break
            except Exception:
                self._context = None

        if self._context is None:
            await self._playwright.stop()
            self._playwright = None
            raise RuntimeError("\u672a\u627e\u5230\u53ef\u7528\u6d4f\u89c8\u5668\uff0c\u8bf7\u5b89\u88c5 Chrome \u6216 Edge")

        self._page = self._context.pages[0] if self._context.pages else await self._context.new_page()

    async def close(self) -> None:
        if self._context:
            await self._context.close()
        if self._playwright:
            await self._playwright.stop()
        self._context = None
        self._playwright = None
        self._page = None

    async def navigate(self) -> None:
        if self._page is None:
            raise RuntimeError("\u6d4f\u89c8\u5668\u672a\u6253\u5f00")
        await self._page.goto(COLLECTION_PAGE_URL, wait_until="domcontentloaded", timeout=45_000)

    async def authenticated(self) -> bool:
        if self._context is None:
            return False
        cookies = await self._context.cookies("https://www.douyin.com")
        return any(c.get("name") in SESSION_COOKIE_NAMES and c.get("value") for c in cookies)

    async def clear_session(self) -> None:
        if self._context is None:
            raise RuntimeError("\u6d4f\u89c8\u5668\u672a\u6253\u5f00")
        await self._context.clear_cookies()
        for p in self._context.pages:
            try:
                await p.evaluate("localStorage.clear(); sessionStorage.clear()")
            except Exception:
                continue

    async def fetch_test(self) -> dict[str, Any]:
        """\u8c03\u7528 listcollection API \u9a8c\u8bc1\u767b\u5f55\u6709\u6548\u6027"""
        if self._page is None:
            raise RuntimeError("\u6d4f\u89c8\u5668\u672a\u6253\u5f00")
        result = await self._page.evaluate(
            """async ({apiUrl}) => {
                var params = new URLSearchParams({
                    device_platform: "webapp", aid: "6383", channel: "channel_pc_web",
                    cookie_enabled: String(navigator.cookieEnabled),
                    browser_language: navigator.language || "zh-CN",
                    browser_platform: navigator.platform || "",
                    browser_name: "Chrome",
                });
                var body = new URLSearchParams({count: "1", cursor: "0"});
                var r = await fetch(apiUrl + "?" + params.toString(), {
                    method: "POST", credentials: "include",
                    headers: {"Content-Type": "application/x-www-form-urlencoded"},
                    body: body.toString(),
                });
                var data = await r.json();
                return {ok: data.status_code === 0};
            }""",
            {"apiUrl": API_URL},
        )
        return result


# ---- \u516c\u5171\u63a5\u53e3 ----

async def _login(timeout_seconds: int = 300, channel: str | None = None) -> dict[str, Any]:
    session = BrowserSession(channel=channel)
    await session.open(headless=False)
    try:
        await session.navigate()
        deadline = asyncio.get_running_loop().time() + timeout_seconds
        while asyncio.get_running_loop().time() < deadline:
            if await session.authenticated():
                result = await session.fetch_test()
                if result.get("ok"):
                    return {"status": "ok", "message": "\u767b\u5f55\u6210\u529f"}
            await asyncio.sleep(2)
        raise TimeoutError(f"\u767b\u5f55\u8d85\u65f6\uff08{timeout_seconds}\u79d2\uff09\uff0c\u8bf7\u91cd\u8bd5")
    finally:
        await session.close()


def login(timeout_seconds: int = 300, channel: str | None = None) -> dict[str, Any]:
    """\u6253\u5f00\u6d4f\u89c8\u5668\uff0c\u7b49\u5f85\u7528\u6237\u624b\u52a8\u767b\u5f55\u6296\u97f3"""
    if timeout_seconds < 10:
        raise ValueError("\u767b\u5f55\u8d85\u65f6\u81f3\u5c11 10 \u79d2")
    return asyncio.run(_login(timeout_seconds=timeout_seconds, channel=channel))


async def _status(channel: str | None = None) -> dict[str, Any]:
    session = BrowserSession(channel=channel)
    await session.open(headless=True)
    try:
        await session.navigate()
        if not await session.authenticated():
            return {"status": "login_required", "message": "\u672a\u767b\u5f55\uff0c\u8bf7\u8fd0\u884c login"}
        result = await session.fetch_test()
        if result.get("ok"):
            return {"status": "authenticated", "message": "\u5df2\u767b\u5f55"}
        return {"status": "login_required", "message": "\u767b\u5f55\u5df2\u8fc7\u671f\uff0c\u8bf7\u91cd\u65b0\u767b\u5f55"}
    finally:
        await session.close()


def status(channel: str | None = None) -> dict[str, Any]:
    """\u68c0\u67e5\u767b\u5f55\u72b6\u6001\uff08\u9759\u9ed8\u6a21\u5f0f\uff09"""
    return asyncio.run(_status(channel=channel))


async def _logout(channel: str | None = None) -> dict[str, Any]:
    session = BrowserSession(channel=channel)
    await session.open(headless=True)
    try:
        await session.clear_session()
        return {"status": "ok", "message": "\u5df2\u767b\u51fa"}
    finally:
        await session.close()


def logout(channel: str | None = None) -> dict[str, Any]:
    """\u6e05\u9664\u767b\u5f55\u6001"""
    return asyncio.run(_logout(channel=channel))


async def ensure_authenticated(channel: str | None = None) -> BrowserSession:
    """\u786e\u4fdd\u5df2\u767b\u5f55\uff0c\u8fd4\u56de\u5df2\u6253\u5f00\u7684 BrowserSession\uff08\u9759\u9ed8 headless=True\uff09"""
    session = BrowserSession(channel=channel)
    await session.open(headless=True)
    await session.navigate()
    if not await session.authenticated():
        await session.close()
        raise RuntimeError("\u672a\u767b\u5f55\u6296\u97f3\uff0c\u8bf7\u5148\u8fd0\u884c: python browser_login.py login")
    result = await session.fetch_test()
    if not result.get("ok"):
        await session.close()
        raise RuntimeError("\u6296\u97f3\u767b\u5f55\u5df2\u8fc7\u671f\uff0c\u8bf7\u91cd\u65b0\u767b\u5f55: python browser_login.py login")
    return session


# ---- CLI ----

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="\u6296\u97f3\u6d4f\u89c8\u5668\u767b\u5f55\u7ba1\u7406")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("login", help="\u6253\u5f00\u6d4f\u89c8\u5668\u767b\u5f55\u6296\u97f3")
    sub.add_parser("status", help="\u68c0\u67e5\u767b\u5f55\u72b6\u6001")
    sub.add_parser("logout", help="\u6e05\u9664\u767b\u5f55\u6001")

    args = parser.parse_args()

    if args.command == "login":
        print(login())
    elif args.command == "status":
        print(status())
    elif args.command == "logout":
        print(logout())
