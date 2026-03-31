# pip install playwright && playwright install chromium
# 任务：TestV2
# 录制时间：2026-03-29 10:36:20
# 由 OpenClaw RPA Recorder（headed 真实录制）生成 — 可脱离 OpenClaw 独立运行

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

CONFIG = {
    "output_dir":    Path.home() / "Desktop",
    "headless":      False,
    "timeout":       60_000,
    "slow_mo":       300,
    # 导航后等待 SPA 内容渲染的额外时间（重型 SPA 如 Yahoo Finance 需要 1-2 秒）
    "spa_settle_ms": 1_500,
    # extract_text 等待目标元素出现的超时（毫秒）
    "content_wait":  15_000,
}

_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

_EXTRACT_JS = (
    "([s,n])=>{return Array.from(document.querySelectorAll(s))"
    ".slice(0,n).map(e=>(e.textContent||'')"
    ".replace(/\\s+/g,' ').trim()).filter(Boolean)}"
)


async def _wait_for_content(page, selector: str) -> None:
    """等待 selector 对应的元素出现在 DOM 中（容错：超时也继续）。"""
    try:
        await page.wait_for_selector(selector, timeout=CONFIG["content_wait"])
    except Exception:
        pass  # 元素未出现也继续，evaluate 会返回空列表


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
            # ── 步骤 1：打开雅虎财经香港
            try:
                await page.goto('https://hk.finance.yahoo.com', wait_until="domcontentloaded")
                await page.wait_for_timeout(CONFIG["spa_settle_ms"])
            except Exception:
                await page.screenshot(path="step_1_error.png")
                raise

            # ── 步骤 2：在搜索框输入NVDA
            try:
                await page.locator('#ybar-sbq').first.fill('NVDA')
            except Exception:
                await page.screenshot(path="step_2_error.png")
                raise

            # ── 步骤 3：点击搜索按钮
            try:
                await page.locator('#ybar-search').first.click()
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(800)
            except Exception:
                await page.screenshot(path="step_3_error.png")
                raise

            # ── 步骤 4：向下滚动触发新闻列表懒加载
            try:
                await page.evaluate("window.scrollBy(0, 1000)")
                await page.wait_for_timeout(600)
            except Exception:
                await page.screenshot(path="step_4_error.png")
                raise

            # ── 步骤 5：继续向下滚动查找新闻区块
            try:
                await page.evaluate("window.scrollBy(0, 1500)")
                await page.wait_for_timeout(600)
            except Exception:
                await page.screenshot(path="step_5_error.png")
                raise

            # ── 步骤 6：提取前 5 条新闻标题存至桌面
            try:
                _sel = '#nimbus-app li'
                _lim = 5
                await _wait_for_content(page, _sel)
                _texts = await page.evaluate(_EXTRACT_JS, [_sel, _lim])
                _out = CONFIG["output_dir"] / 'news.txt'
                _out.write_text("\n".join(_texts), encoding="utf-8")
                print(f"已提取 {{len(_texts)}} 条，写入 {{_out}}")
            except Exception:
                await page.screenshot(path="step_6_error.png")
                raise

        except PlaywrightTimeout as e:
            await page.screenshot(path="error_timeout.png")
            raise RuntimeError(f"超时：{e}") from e
        except Exception:
            await page.screenshot(path="error_unexpected.png")
            raise
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
