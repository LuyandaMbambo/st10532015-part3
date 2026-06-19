import asyncio
from urllib.parse import quote
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = 'http://127.0.0.1:8000'
PAGES = [
    'index.html',
    'about.html',
    'contact.html',
    'get involved.html',
    'programs.html',
]

OUT_DIR = Path('screenshots')
OUT_DIR.mkdir(exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for fname in PAGES:
            url = f"{ROOT}/{quote(fname)}"
            print('Loading', url)
            try:
                await page.goto(url, wait_until='networkidle')
                # wait a short time for JS (e.g., navbar/main) to run
                await page.wait_for_timeout(600)
                out_name = fname.replace(' ', '-').replace('.html','') + '.png'
                out_path = OUT_DIR / out_name
                await page.screenshot(path=str(out_path), full_page=True)
                print('Saved', out_path)
            except Exception as e:
                print('Failed', fname, e)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
