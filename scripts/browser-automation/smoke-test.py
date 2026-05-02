"""Playwright on しゅん先生 PC - smoke test"""
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://example.com', wait_until='domcontentloaded')
        title = await page.title()
        url = page.url
        print(f"OK: title={title!r} url={url}")
        await page.screenshot(path=r'C:\Users\wirel\Desktop\playwright-smoke.png')
        print(f"screenshot saved")
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
