import asyncio, json, os
from playwright.async_api import async_playwright

profile_dir = os.path.join(os.environ["LOCALAPPDATA"], "douyin-favorites-to-knowledge", "browser-profile")

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            viewport={"width": 1280, "height": 800},
            locale="zh-CN"
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://www.douyin.com/user/self?showTab=favorite_collection", wait_until="domcontentloaded", timeout=45000)
        await asyncio.sleep(5)

        # Get page text to find Ai folder
        text = await page.evaluate("() => document.body.innerText.substring(0, 5000)")
        print("Page text sample:", text[:2000])

        # Take screenshot for debugging
        await page.screenshot(path=r"D:\my_knowledgebase\tools\douyin_page.png")
        print("Screenshot saved")

        # Try clicking elements with 'Ai' text
        clicked = await page.evaluate("""() => {
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            let node;
            const found = [];
            while (node = walker.nextNode()) {
                if (node.textContent.trim() === "Ai" || node.textContent.trim() === "AI") {
                    found.push({text: node.textContent.trim(), parent: node.parentElement.tagName, parentClass: node.parentElement.className});
                }
            }
            return found;
        }""")
        print("Ai elements found:", json.dumps(found, ensure_ascii=False))

        await context.close()

asyncio.run(main())
