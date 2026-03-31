# openclaw-rpa

OpenClaw RPA skill: **headed browser recording**, plan-based steps, and **standalone Playwright Python** scripts.

## Requirements

- **Python 3.8+** (3.10+ recommended)
- **pip** and network access for `pip install` and Playwright browser downloads

## Install (recommended)

From this directory:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

This creates a **`.venv`**, installs Python dependencies from `requirements.txt`, and runs **`playwright install chromium`**.

Then activate the venv whenever you work with this skill:

```bash
source .venv/bin/activate
```

### Manual install

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
python -m playwright install chromium
```

### Check environment

```bash
python3 envcheck.py
# or
python3 rpa_manager.py env-check
```

`record-start` and `run` also verify Python + Playwright and **auto-install Chromium** when possible (same behavior as before).

## First-time config (locale)

The repo ships **`config.example.json`** only (default **`en-US`**).

```bash
python3 scripts/bootstrap_config.py
```

This creates **`config.json`** from the example. Edit `"locale"` or use:

```bash
python3 scripts/set_locale.py zh-CN
python3 scripts/set_locale.py en-US
```

See **`LOCALE.md`** for details. After changing locale, start a new OpenClaw session or re-read **`SKILL.md`** / **`SKILL.*.md`**.

## Quick start (CLI)

```bash
python3 rpa_manager.py env-check
python3 rpa_manager.py list
python3 rpa_manager.py run wikipedia
```

Recorder flow: `record-start` → `record-step` → `record-end` (see `rpa_manager.py` docstring).

## Sample scripts

Pre-generated scripts and command logs live under **`rpa/`**. Good starting points:

| Script | Notes |
|--------|--------|
| `rpa/wikipedia.py` | Stable public site (English) |
| `rpa/wiki.py` | Same flow, alternate naming |
| `rpa/豆瓣电影.py` | Chinese demo (site policies apply) |
| `rpa/电商网站购物v10.py` | E-commerce style demo (example only) |

**examples/README.md** lists curated recommendations and cautions.

## Publish to GitHub

Create an **empty** public repository on GitHub, then:

```bash
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

## License

MIT — see `LICENSE`.
