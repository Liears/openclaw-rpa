# Example RPA scripts (`../rpa/`)

These are **sample outputs** from the recorder. They are **not** guaranteed to run forever (sites change, login walls, rate limits).

## Suggested first runs

1. **`wikipedia.py`** / **`wiki.py`** — Public Wikipedia, good for verifying Playwright + headless run.
2. **`豆瓣电影.py`** — Chinese UI example; respect the site’s terms of service.

## Heavier / scenario demos

- **`电商网站购物*.py`** — Shopping-flow demos; **do not** use for production scraping without permission.
- **`每日美股快报整理*.py`** — News-style workflows; **verify** sources and compliance.

## Command logs

Each `*.py` may have a sibling `*_playwright_commands.jsonl` recording the step log used during synthesis.
