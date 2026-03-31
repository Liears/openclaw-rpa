# pip install playwright && playwright install chromium
# 任务：每日美股快报整理V5
# 生成时间：2026-03-28 12:19:03
# 由 OpenClaw RPA 引擎自动生成 — 可脱离 OpenClaw 独立运行

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ── 配置区（修改此处即可适配不同环境）──────────────────────
CONFIG = {
    "output_dir": Path.home() / "Desktop",  # 文件输出目录
    "headless": False,                       # True = 无头模式
    "timeout": 60_000,                       # 超时毫秒
    "slow_mo": 300,                          # 操作间隔 ms，模拟人类速度
}

# ── 反爬虫：伪造真实浏览器特征 ────────────────────────────
_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


# ── 主流程 ────────────────────────────────────────────────
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=CONFIG["headless"],
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            slow_mo=CONFIG["slow_mo"],
        )
        context = await browser.new_context(
            user_agent=_UA,
            viewport={"width": 1440, "height": 900},
            locale="en-US",
            timezone_id="America/New_York",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        await context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        page = await context.new_page()
        page.set_default_timeout(CONFIG["timeout"])

        try:
            # 步骤 1：打开雅虎财经 hk.finance.yahoo.com
            try:
                await page.goto('https://hk.finance.yahoo.com', wait_until="domcontentloaded")
            except Exception:
                await page.screenshot(path="step_1_error.png")
                raise

            # 步骤 2：搜索 NVDA
            try:
                await page.locator('input[type="text"]').first.fill('NVDA')
                await page.keyboard.press("Enter")
                await page.wait_for_load_state("domcontentloaded")
            except Exception:
                await page.screenshot(path="step_2_error.png")
                raise

            # 步骤 3：提取前五条新闻标题并存到桌面 news.txt
            try:
                # TODO: 实现 read 操作，目标：Top 5 news titles
                pass
            except Exception:
                await page.screenshot(path="step_3_error.png")
                raise

        except PlaywrightTimeout as e:
            await page.screenshot(path="error_timeout.png")
            raise RuntimeError(f"操作超时，截图已保存: {e}") from e
        except Exception:
            await page.screenshot(path="error_unexpected.png")
            raise
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
