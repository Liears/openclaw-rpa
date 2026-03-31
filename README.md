# openclaw-rpa

English | **[中文](README.zh-CN.md)**

## Demo video

Sauce Demo ([saucedemo.com](https://www.saucedemo.com)) e-commerce screen recording.

> **Note:** Bilibili `<iframe>` cannot be embedded in README. For **GitHub-native video**, use the compressed file **`saucedemo-readme.mp4`** (≤10MB): drag it into an **Issue/PR comment**, copy the generated Markdown into README for inline playback ([docs](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files)). Or open **[blob preview](https://github.com/laziobird/openclaw-rpa/blob/main/saucedemo-readme.mp4)** for GitHub’s player.

### [▶ Watch on Bilibili (BV1YfXrBBE9u)](https://www.bilibili.com/video/BV1YfXrBBE9u/)

<p align="center">
  <a href="https://www.bilibili.com/video/BV1YfXrBBE9u/"><img src="https://img.shields.io/badge/bilibili-Watch_demo-00A1D6?style=for-the-badge&logo=bilibili&logoColor=white" alt="Watch on Bilibili"></a>
</p>

<p align="center">
  <sub>
    Compressed demo: <a href="saucedemo-readme.mp4"><code>saucedemo-readme.mp4</code></a> (~7.7MB, H.264) ·
    <a href="https://github.com/laziobird/openclaw-rpa/blob/main/saucedemo-readme.mp4">GitHub preview</a>
    · <a href="https://github.com/laziobird/openclaw-rpa/raw/main/saucedemo-readme.mp4">raw</a>
  </sub>
</p>

**Steps in the video (conversation)**

1. Send **`#rpa`** / **`#RPA`**, or a message containing **`RPA`** / **“automation robot”** — see [**SKILL.md**](SKILL.md) and [**SKILL.en-US.md** — Trigger detection](SKILL.en-US.md#trigger-detection).
2. Task name examples: **`电商网站购物`**, or match an existing script like **`电商网站购物V10`** (see **`registry.json`**).

**Task prompt**

1. Open `www.saucedemo.com`, sign in **`standard_user`** / **`secret_sauce`**.  
2. Sort **price high → low**.  
3. Add the **two most expensive** items to the cart.  
4. **Log out**.

Full protocol: [**SKILL.en-US.md**](SKILL.en-US.md) (ONBOARDING, RECORDING). Replay: `run:{task}` or `python3 rpa_manager.py run <name>`.

---

> With **AI assistance**, record **typical website** and **local file** workflows into a **repeatable Playwright Python** script. **Replay without the LLM on every run**—saves compute and keeps steps deterministic (vs. ad-hoc model calls).

| | |
|:---|:---|
| **Needs** | Python **3.8+**, network for `pip` / Playwright browsers |
| **License** | [Apache 2.0](LICENSE) |

---

## Quick install (OpenClaw)

Put the skill here: **`~/.openclaw/workspace/skills/openclaw-rpa`**

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/laziobird/openclaw-rpa.git ~/.openclaw/workspace/skills/openclaw-rpa
cd ~/.openclaw/workspace/skills/openclaw-rpa

chmod +x scripts/install.sh && ./scripts/install.sh
python3 scripts/bootstrap_config.py
python3 scripts/set_locale.py zh-CN    # or: en-US

python3 rpa_manager.py env-check
```

**SSH clone:** `git@github.com:laziobird/openclaw-rpa.git`

After install, **start a new OpenClaw chat** (or reload skills) so the agent reads **`SKILL.md`**. Triggers and keywords: **`SKILL.md`** (e.g. `#RPA`, “automation robot”).

---

## Advanced

<details>
<summary><b>Manual install · gateway Python · paths · publishing</b></summary>

### Manual install (no `install.sh`)

```bash
cd /path/to/openclaw-rpa
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt
python -m playwright install chromium
```

### Which `python` does OpenClaw use?

`rpa_manager.py` uses **`sys.executable`**. That interpreter must have **Playwright**. If the gateway uses **system** `python3`, install deps there **or** point tools at:

`~/.openclaw/workspace/skills/openclaw-rpa/.venv/bin/python`

### Locale & `config.json`

- **`SKILL.md`** → `metadata.openclaw.localeConfig` → **`config.json`**
- If `config.json` is missing, the router can use **`config.example.json`** for `locale`
- Details: **`LOCALE.md`**

### Paths in `SKILL.en-US.md` / `SKILL.zh-CN.md`

Examples may use `~/.openclaw/workspace/skills/openclaw-rpa/`. Change the prefix if your workspace differs.

### Publish the skill

**[ClawHub — publish a skill](https://clawhub.ai/publish-skill)** (link this GitHub repo).

### Environment check

```bash
python3 envcheck.py
# or
python3 rpa_manager.py env-check
```

`record-start` / `run` can auto-install Chromium if missing.

</details>

---

## CLI quick start

```bash
python3 rpa_manager.py env-check
python3 rpa_manager.py list
python3 rpa_manager.py run wikipedia
```

Recorder: `record-start` → `record-step` → `record-end` (see `rpa_manager.py` docstring).

---

## Sample scripts (`rpa/`)

| Script | Notes |
|--------|--------|
| `wikipedia.py` / `wiki.py` | Wikipedia (English) |
| `豆瓣电影.py` | Chinese UI demo (follow site rules) |
| `电商网站购物v10.py` (and related) | Sauce Demo flow (same as the [demo video](#demo-video) at the top) |

More notes: **`examples/README.md`**.

---

<p align="center">
  <sub>Apache License 2.0 · Copyright © 2026 openclaw-rpa contributors</sub>
</p>
