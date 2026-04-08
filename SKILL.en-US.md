---
name: openclaw-rpa
language: en-US
description: Record browser & local-file actions once; replay runs without the LLM—save $ vs AI browsing, faster, no hallucinations. github.com/laziobird/openclaw-rpa
metadata: {"openclaw": {"emoji": "🤖", "os": ["darwin", "linux"]}}
---

> **This file:** `en-US` (selected by `locale` in [config.json](config.json) or [config.example.json](config.example.json) if `config.json` is missing; Chinese: [SKILL.zh-CN.md](SKILL.zh-CN.md))

> **GitHub:** **[https://github.com/laziobird/openclaw-rpa](https://github.com/laziobird/openclaw-rpa)** — install, `rpa/` samples, issues

# openclaw-rpa

**Example automations** (illustrative; **obey each site’s terms of use and applicable law**): **e‑commerce login & shopping**; **Scenario 1** (below) **quotes API + news page + local brief**; **Yahoo Finance** browser-only quotes / news; movie sites **reviews & ratings** in one scripted run; **AP reconciliation** (GET-only mock API, local Excel vs invoices, **Word table** report — no ERP submit) — **[EN](articles/scenario-ap-reconciliation.en-US.md)** · **[中文](articles/scenario-ap-reconciliation.md)**.

## What this skill does

**openclaw-rpa** is a **Recorder → Playwright script** pipeline: the agent drives a real browser, you confirm steps, and **`record-end`** compiles a **normal Python** file under `rpa/`. **Replay** runs that file with **`rpa_manager.py run`**—**no** LLM per click.

**Highlights**

1. **Saves compute and money** — Letting a **large model** operate the browser **every** time can cost **on the order of single-digit to tens of US dollars** per heavy session (tokens, tools, long context). After you **record once**, repeat runs **do not invoke the model**—cost is essentially **local script execution**, and runs are **much faster** than step-by-step LLM reasoning.
2. **Verify the flow once, then run the same steps every time** — During recording you **prove** the task works; replay **executes the saved steps** deterministically. You avoid asking the AI to improvise on each run, which **reduces inconsistency** and **hallucination-driven** mistakes.

**Recommended LLM:** Minimax 2.7 · Google Gemini Pro 3.0 and above · Claude Sonnet 4.6

Output is **ordinary Python**; after **`record-end`** you may still patch helpers (`pathlib` / `shutil` / `open()`, or **`extract_text`** during recording)—browser-only, file-only, or both.

## When to use

| Goal | What to send |
|------|----------------|
| **Start recording** a new flow | `#automation robot`, `#RPA`, `#rpa`, or mention **Playwright automation** |
| **Record a flow with an HTTP API** | `#rpa-api` (describe the API or paste an API doc param block `###...###` in the message) |
| **List saved tasks** | `#rpa-list` |
| **Run a saved task** (e.g. new chat) | `#rpa-run:{task name}` |
| **Run in this chat** | `run:{task name}` |
| **Schedule / reminder** (OpenClaw + IM) | Natural language + `#rpa-run:…` — depends on your gateway |

## Quick start

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py list   # same as #rpa-list
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py run "your-task-name"
```

In chat, prefer **`#rpa-list`** → **`#rpa-run:your-task-name`** so names match `registry.json`.

### Running recorded scripts (reminder)

- **`#rpa-list`** — shows **registered** task names; use **first** if unsure.
- **`#rpa-run:{task}`** / **`run:{task}`** — **execute the saved script again**; they do **not** start a new recording.

## Scope (details)

**In the browser** — Clicks, typing, selects, scroll, wait, screenshots; multi-step flows are first-class. Extracting page text is **one** option.

**On disk (optional)** — While recording, **`extract_text`** can write text under the user’s home. After **`record-end`**, edit `rpa/*.py` per [playwright-templates.md](playwright-templates.md).

**Out of scope** — Large ETL, databases, or heavy OS automation.

### Examples (illustrative)

| Pattern | Example |
|---------|---------|
| **Browser only** | **E‑commerce:** login → browse → cart/checkout (`rpa/电商网站购物*.py` style). **Yahoo Finance:** quotes / headlines. **Movies:** aggregate **reviews & ratings**. |
| **Browser then files** | Same flow, plus **`extract_text`** when asked. |
| **Browser + HTTP API + files** | **Scenario 1:** **`api_call`** (e.g. [Alpha Vantage TIME_SERIES_DAILY](https://www.alphavantage.co/documentation/#daily)) saves JSON/text locally, then **`goto` + `extract_text`** for a brief. |
| **HTTP API + Excel + Word (browser optional)** | **AP reconciliation:** mock **GET** batches, local sheets, **no submit**; output **.docx** with tables — see **[EN](articles/scenario-ap-reconciliation.en-US.md)** · **[中文](articles/scenario-ap-reconciliation.md)**. |
| **Files only in script** | After **`record-end`**, add folder cleanup—**no URL** for that block. |

## Recommended sites for getting started

**Good fits — predictable structure, works well out of the box:**

| Category | Examples |
|----------|---------|
| **Finance / data** | Yahoo Finance (quotes, headlines), Google Finance, investing.com |
| **E-commerce** | Sauce Demo (`saucedemo.com`), AliExpress product pages, eBay search results |
| **News / media** | BBC News, Reuters, Hacker News, Reddit (listing pages) |
| **Reference** | Wikipedia, GitHub (public repo pages, issues list) |
| **Job boards** | LinkedIn Jobs (public search), Indeed results page |
| **Travel / weather** | weather.com, Google Flights results (read-only) |
| **Demo / test sites** | `the-internet.herokuapp.com`, `demoqa.com`, `automationpractice.pl` |

**Not recommended — likely to break or require manual workarounds:**

| Situation | Why |
|-----------|-----|
| **Highly dynamic SPAs** (heavy client-side routing, frequent DOM mutations) | Selectors shift between renders; snapshots may miss unrendered content |
| **CAPTCHA / bot-detection sites** (Google reCAPTCHA, hCaptcha, Cloudflare Turnstile) | Automation will be blocked; human intervention required |
| **Login-gated flows without saved sessions** | Credentials and 2FA must be handled manually before replay |
| **Infinite-scroll feeds with no stable IDs** | Progressive probing helps but results are inconsistent |

> **Tip:** when trying a new site, start with a simple `goto` + `snapshot` step to check whether the page structure is readable before building a full flow.

---

## Troubleshooting: `LLM request timed out` (not the record-step timeout)

If logs show `error=LLM request timed out`, `model=gemini-...`, `provider=google`:

| Meaning | A **single** OpenClaw → LLM API call (reply generation + tool planning) exceeded the gateway/client **LLM timeout**. This is **not** the `record-step` wait for a result (e.g. 120s) and **not** Chromium navigation timeout. |
| Common causes | **Too much in one turn**: multiple `record-step` calls / long reasoning / pasting the full page snapshot back into the reply; oversized context and output; slower models (e.g. `gemini-3-pro-preview`) plus the tool chain. |
| Skill-side | **Must** follow the anti-timeout rules below: after `plan-set`, advance **only a small slice per user turn** (≤2 `record-step` calls), keep replies short, and **do not** paste full snapshot JSON into the chat repeatedly. |
| Environment | **Raise the LLM request timeout** in OpenClaw/Gateway if the product exposes it; unstable network to the Google API also increases latency. |

---

## Trigger detection

On each user message, **check in this order** (**first match wins**; do not skip order or `#rpa-list` may be mistaken for ONBOARDING because it contains `#rpa`; `#rpa-api` must be checked before the generic `#rpa`):

| Order | Condition | State |
|:-----:|-----------|--------|
| 1 | Message is a **RUN** (see table below) | RUN |
| 2 | After trim, message **equals** `#rpa-list` (**case-insensitive**, e.g. `#RPA-LIST`) | LIST |
| 3 | Message contains **`#rpa-api`** (case-insensitive) | RPA-API |
| 4 | Message contains **#automation robot** OR **#RPA** OR **#rpa** (case-insensitive for `#RPA` / `#rpa`) | ONBOARDING |

Intercept and handle these; do not run the raw user task outside this skill.

**RUN triggers (order 1):**

| Form | Notes |
|------|--------|
| `#rpa-run:{task name}` | **Run in a new chat** (no reliance on this thread): after trim, message **starts with** `#rpa-run:` (**case-insensitive**, e.g. `#RPA-RUN:`). **After the first colon** to **end of line** is `{task name}` (**must match** a name from `#rpa-list`, trimmed). |
| `run:{task name}` | **Run in this chat:** `run:` then optional spaces, then task name to end of line (trimmed; same name rules). |

> **`zh-CN` locale:** use [SKILL.zh-CN.md](SKILL.zh-CN.md) (`#自动化机器人`, `#RPA` / `#rpa`, `#rpa-list`, `#rpa-run:`, `#运行:`).

---

## State machine

```
IDLE ──trigger──► ONBOARDING (show signup rules)
                    │
                    └──one user message ("task name LETTER" or two-line)──► DEPS_CHECK
                                                                                      │
                    ┌───────────────────────────────────────────────────────────────┘
                    │  python3 rpa_manager.py deps-check <letter>
                    ├─failed + user sends CANCEL (fixed token)──────────────────────► IDLE (abort)
                    ├─failed + user sends AGREE──deps-install──deps-check again───────┐
                    └─passed ──────────────────────────────────────────────────────┤
                                                                                       ▼
                                                                                RECORDING
RECORDING ──end recording──► GENERATING ──► IDLE
    │abort
    └────────────────────────────────────► IDLE
IDLE ──"#rpa-api"──► RPA-API ──parsed──► (same task+capability rules)──► DEPS_CHECK ──► RECORDING …
IDLE ──"#rpa-run:{task}" / "run:{task}"──► RUN ──► IDLE
IDLE ──"#rpa-list"──► LIST ──► IDLE
```

> **Note:** For codes **B / C / F / N**, **`record-start` does NOT open Chrome** — no browser is launched. The agent issues `excel_write`, `word_write`, `api_call`, `merge_files`, `python_snippet` steps directly without any browser window.

---

## RPA-API state

Triggered by: message contains **`#rpa-api`** (case-insensitive).

### ⛔ Absolute prohibitions (agent MUST enforce)

> **Do NOT call the HTTP API yourself. Do NOT run Python / httpx / requests / curl. Do NOT return the API response to the user.**  
> The **sole purpose** of `#rpa-api` is to **record the API call into a replayable RPA script** — exactly like `#rpa` / `#automation robot` does for browser actions.  
> No matter how trivial the API call looks, it **must** go through `record-start` → `record-step api_call` → `record-end`.  
> **Fetching data "on behalf of the user" without recording is a violation.**

### Output the following verbatim — do not skip

```
🤖 OpenClaw RPA recorder ready (API + browser mode)

I'll record your API call and browser steps into a replayable RPA script.
Future runs just execute the script — no model needed to fetch data every time.

How it works:
1. I parse the API info you provided → key is written directly into the script (no export needed)
2. Browser / file steps run in a real Chrome window with screenshots for confirmation
3. Say "end recording" → compile into a standalone Playwright Python script

Send one message: line 1 = task name, line 2 = capability letter **A–G** or **N** (see `#automation robot` / `#RPA` onboarding table).
```

### Parsing the `###...###` API declaration block

Wrap API info in `###` markers. Two accepted formats:

**Format A — natural language + API doc URL + key**
```
###
Task description (e.g.: fetch NVDA daily OHLCV, save to Desktop as nvda_time_series_daily.json)
API docs  https://www.alphavantage.co/documentation/#daily
API key   YOUR_API_KEY
###
```

**Format B — paste API doc parameter snippet + key**
```
###
API Parameters
❚ Required: function    → TIME_SERIES_DAILY
❚ Required: symbol      → IBM
❚ Required: apikey
Example: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
apikey  YOUR_API_KEY
###
```

Both formats can be mixed. Lines **outside** the block are the subsequent **browser / file steps**.

### Agent steps (in order — none may be skipped or merged)

**Step 0 — Output the greeting and wait for “task name + capability”** (same format as **ONBOARDING**: `task name LETTER` on one line, or two-line compatible). If the user already included it in the same message as `#rpa-api`, go straight to **DEPS_CHECK**.

**Step 1 — Extract API info from the block**  
   - Identify: **base_url**, **required params** (function, symbol, …), **key field name** (apikey / token / key / …)  
   - If a doc URL is given, infer base_url + function from URL path + params; fill business params (symbol, etc.) from the user description  
   - Save filename from user description → **`save_response_to`**

**Step 2 — Embed the key into the script (when provided)**  
   - Name the env var from the API provider (examples: Alpha Vantage → `ALPHAVANTAGE_API_KEY`; OpenAI → `OPENAI_API_KEY`; custom → `MY_API_TOKEN`)  
   - In the `record-step` JSON:
     - Use **`__ENV:VAR_NAME__`** placeholder in `params` / `headers`  
     - **Also** put the real key in the step's **`"env"`** field:  
       ```json
       {
         "action": "api_call",
         ...,
         "params": {"apikey": "__ENV:ALPHAVANTAGE_API_KEY__", ...},
         "env": {"ALPHAVANTAGE_API_KEY": "user-supplied-real-key"}
       }
       ```
   - When `env` is present, the code generator writes the key **directly into the script** (e.g. `'apikey': 'UXZ3BOXOH817CQWS'`) — **no `export` required** for replay  
   - **Do NOT** output an `export VAR=…` instruction; instead confirm: "Key written directly into the script — no setup needed before replay."  
   - If the user **did not** supply a key, omit `env`, use placeholder only, and tell the user they'll need `export VAR_NAME=…` before running

**Step 3 — After “task name + capability” and DEPS_CHECK, start recording**  
   - Run `record-start "{task name}" --profile {LETTER}` (same capability rules as ONBOARDING; `deps-check` must pass first)  
   - After `✅ Recorder ready`, inject `api_call` as the **first step** (key in the `env` field):
     ```bash
     python3 rpa_manager.py record-step '{"action":"api_call","context":"...","base_url":"...","params":{...,"key_field":"__ENV:VAR_NAME__"},"env":{"VAR_NAME":"real_key"},"method":"GET","save_response_to":"..."}'
     ```
   - Confirm result to the user (screenshot / file written)

**Step 4 — Continue with steps outside the block**  
   Follow the RECORDING single-step protocol for browser steps, `merge_files`, etc., until the user sends `#end-recording` / `end recording`.

> **No `###` block:** if the message is only `#rpa-api` with no block, output the greeting, ask for task name + capability (`task name LETTER` on one line, or two-line; same as ONBOARDING) → **DEPS_CHECK** → **RECORDING** — the user issues `api_call` steps manually.

## ONBOARDING

**Output the following verbatim (English):**

```
🤖 OpenClaw RPA lab ready

With AI help, we’ll record what you do in a real browser (and local file steps if you need them) and compile it into an RPA script you can run again and again.
Later runs use that script directly—no need for the model to drive every click—saving compute and keeping steps consistent (vs. LLM hallucinations on fragile actions).

── Sign-up (one message) ──
Format:  Task name  Capability code
Example: reconciliation  F

Capability code (one trailing uppercase letter):
  A  Browser only
  B  Excel only (.xlsx via openpyxl; no Microsoft Excel app required)
  C  Word only (.docx via python-docx; no Microsoft Word app required)
  D  Browser + Excel
  E  Browser + Word
  F  Excel + Word (no web steps in the task)
  G  Browser + Excel + Word
  N  None of the above (e.g. API + merge text files only)

Excel / Word (plain language):
• Usually OK: multiple sheets, data, headers, column width, freeze top row, hidden columns; Word templates, paragraphs, simple tables.
• Not a good fit: macros, pivot refresh, heavy formula evaluation without Excel; Word track-changes, complex fields, legacy .doc.

Dependencies install into the **same Python** you use for Playwright / this skill. If something is missing, I'll ask before installing.

After recording starts:
1. Send instructions → I run real browser steps when the flow uses the web, with screenshots.
2. Say "end recording" → compile the RPA script.

Common commands:
• "end recording" → generate the script (see GENERATING for Office append rules)
• "abort" → close the browser and discard this session
• Multi-step plans: **continue**, **1**, **next** (same as "ok", "y", "go")
• HTTP API: **`api_call`** during recording, or start with **`#rpa-api`**.
• Help / view all commands: start with **`#rpa-help`**.

Good sites: Yahoo Finance, BBC News, Hacker News, GitHub public pages, Wikipedia.
Not recommended: CAPTCHAs, or highly dynamic SPAs.

Send: task name + capability letter (e.g. "reconciliation  F")
```

---

## DEPS_CHECK (after onboarding signup)

**Parse the user message**

1. **Single-line format** (preferred): after trimming, if the **last whitespace-separated token** is a single character `A`–`G` or `N` (case-insensitive → uppercase) → capability; **everything before it** trimmed → `{task name}`.  
2. **Two-line format** (compatible): split into lines, last non-empty line is single letter → capability; all previous lines joined → `{task name}`.  
3. If neither format yields a valid capability letter → do **not** `record-start`; show corrected example `Supplier reconciliation sheet F` and ask the user to resend.  
4. If the user already included the info in the **same trigger message**, skip re-asking.

**Check (same `python3` as Playwright)**

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py deps-check {LETTER}
```

- **Exit 0** → start recording (below) with `--profile`.  
- **Non-zero** → explain what’s missing in plain language, then tell the user there are **exactly two** allowed replies — nothing else counts.

**Fixed options only** (verbatim; copy-paste recommended)

After **trimming leading/trailing whitespace**, the message must be **exactly** one of (ASCII **case-insensitive**):

| Reply | Meaning |
|-------|---------|
| `AGREE` | Run `deps-install {LETTER}` → `deps-check` again → `record-start` if OK |
| `CANCEL` | Abort signup, return to IDLE, do not install |

- If the user sends anything else (`ok`, `yes install`, `go ahead`, …) → **do not** run `deps-install`. Reply: **Send only `AGREE` or `CANCEL` on its own line (no extra words or punctuation).**  
- On **`AGREE`** (any casing) → run `deps-install` → `deps-check` → `record-start` or show stderr.  
- On **`CANCEL`** → IDLE.

Do **not** run `deps-install` unless the trimmed message equals **`AGREE`** ignoring ASCII case.

---

## RECORDING (Recorder mode — headed browser)

### Start recording (after DEPS_CHECK passes)

Run (**always pass `--profile`** matching the signup letter):

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-start "{task name}" --profile {LETTER}
```

When the command prints `✅ Recorder ready`, reply one of the following based on the capability:

**If capability includes a browser (A / D / E / G):**
```
✅ Recording started: 「{task name}」
Capability saved in recorder_session/task.json (needs_excel / needs_word / needs_browser / capability).
🖥️  Chrome is now open — send your first instruction and I will run it in the real browser with a screenshot.
Send your first instruction (I can split multi-step work).
```

**If capability has NO browser (B / C / F / N):**
```
✅ Recording started: 「{task name}」
Capability saved in recorder_session/task.json (needs_excel / needs_word / needs_browser / capability).
📂 No browser — this task uses file / API steps only. Use `excel_write`, `word_write`, `api_call`, `python_snippet`, or `merge_files`.
Send your first instruction.
```

---

### Anti-timeout: multi-step instructions **must** be split — **one step per user turn**

**When to split:** The user’s message contains **two or more** independent atomic actions (navigate, search, click, extract, …).

#### Split workflow

**First turn (multi-step instruction):**

1. Decompose into atomic sub-tasks (each sub-task maps to ≤2 `record-step` calls).
2. Persist the plan with `plan-set`:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py plan-set '["subtask 1", "subtask 2", "subtask 3"]'
   ```
3. Execute **step 1 only** (do not continue).
4. End with:
   ```
   📍 Progress: 1/{N} done
   ✅ [step description]
   📸 Screenshot: {path}
   Confirm the screenshot, then say **continue**, **1**, or **next** to run step 2/{N} (see shortcut confirmations below).
   ```

> **Shortcut confirmations** (all mean “continue to the next step”): `continue`, `1`, `next`, `ok`, `y`, `go` (`next` is case-insensitive). The user may send **`1`** or **`next`** alone — no full sentence required.

**Later turns (after one of the shortcuts):**

1. Check plan progress:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py plan-status
   ```
2. Run the action for the current step (`snapshot` + action, ≤2 `record-step` calls).
3. Advance the plan:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py plan-next
   ```
4. If there is a next step → print progress and wait for confirmation. If all steps are done → print:
   ```
   🎉 All {N} steps completed!
   Say "end recording" to generate the RPA script, or describe more actions.
   ```

> **Why:** Each LLM request should only run **2–3** tool calls; a single `record-step` wait for the recorder can be up to **120s** (same as `rpa_manager` polling). Multi-step work must still be split so total time does not trigger `LLM request timed out`.

---

### Single-step recording protocol (for every user instruction)

#### Step 1: Get current page elements (free, not written to script)
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{"action":"snapshot"}'
```
→ Returns all interactive elements and their **real CSS selectors** (e.g. `#search-input`, `input[name="q"]`, `[aria-label="Search"]`).

#### Step 2: Choose the target CSS from the snapshot
- **Must** use the real `sel` from the snapshot — **do not guess**.
- **Default to progressive probing** (below): do not expect one `snapshot` to cover the whole page; if the target is missing, loop **scroll → wait → snapshot**, and use **`dom_inspect`** when needed.
- If there is no valid selector, the element may be below the fold — `scroll` first, then `snapshot` again.

#### Step 3: Perform an action (pick one)

| action | target | value | Notes |
|--------|--------|-------|--------|
| `goto` | URL string | — | Navigate: `wait_until=domcontentloaded` + 1.5s SPA settle |
| `snapshot` | — | — | Current DOM + content blocks (not logged to script) |
| `fill` | CSS | text | **Only** `<input>` / `<textarea>` — **not** native `<select>` |
| `select_option` | `<select>` CSS | **option value** (see below) | Native `<select>`: `locator.select_option(...)`. Optional `"select_by": "label"` → `value` is visible text; `"index"` → numeric index |
| `press` | Key name e.g. `Enter` | — | Key press, then wait for stability |
| `click` | CSS | — | Click, then wait for stability |
| `scroll` | — | pixels | Scroll down by N pixels |
| `scroll_to` | CSS | — | **Scroll element into view (lazy-load)**, then `wait` + `snapshot` |
| `dom_inspect` | Container CSS | — | **Debug:** list child structure under a container (**not logged** to script); use to infer list/title selectors |
| `extract_text` | CSS | output filename | Text from multiple elements → `~/Desktop/<filename>` |
| `api_call` | — | — | **HTTP** (independent of the page): either full **`url`**, or **`base_url` + `params`**. Optional **`method`** (default `GET`), **`headers`**, **`body`** (POST JSON), **`save_response_to`** (relative path under `~/Desktop`). **Secrets:** in `params` or `headers` string values, use **`__ENV:ENV_VAR_NAME__`** (e.g. `"apikey": "__ENV:ALPHAVANTAGE_API_KEY__"`). **If the step also has an `"env"` field** (e.g. `{"ALPHAVANTAGE_API_KEY":"real_key"}`), the key is **written directly into the generated script** — no `export` needed for replay; omitting `env` generates `os.environ.get("VAR", "")` and requires `export` before replay. |
| `merge_files` | — | — | **Merge Desktop files** (pure local, no browser): **`sources`** (list of filenames under `~/Desktop`), **`target`** (output filename), optional **`separator`** (default `"\n\n"`). Typical use: combine an `api_call` JSON with an `extract_text` news file into a single brief. |
| `excel_write` | — | — | **Write `.xlsx`** (openpyxl; **no Microsoft Excel required**). **`path`** or **`value`**: relative filename (recording writes under **~/Desktop**; generated script uses `CONFIG["output_dir"]`). **`sheet`**: worksheet name. **`headers`**: optional list of header strings. **Row data — pick one**: ① **`rows`**: static 2-D array of cell values; ② **`rows_from_json`**: `{"file":"x.json","outer_key":"batches","inner_key":"lines","fields":["f1","f2"],"parent_fields":["batch_id"]}` — dynamically flatten a nested JSON array from Desktop (`inner_key`/`parent_fields` optional); ③ **`rows_from_excel`**: `{"file":"发票导入_本周.xlsx","sheet":"发票侧","skip_header":true}` — copy data rows from another xlsx sheet. **`freeze_panes`**: optional e.g. `"A2"`. **`hidden_columns`**: optional list of **1-based** column indexes to hide (e.g. `[1]` hides column A). **`replace_sheet`**: default `true` (delete same-named sheet then recreate); `false` appends **`rows`** at the end of an existing sheet. |
| `word_write` | — | — | **Write `.docx`** (python-docx; **no Word app required**). **`path`** or **`value`**: relative filename. **`paragraphs`**: list of strings (one paragraph each). **`table`**: optional — `{"headers": [...], "rows": [[...]]}` inserts a table after paragraphs (auto-applies "Table Grid" style). **`mode`**: `new` (default) or `append` (append to existing file). |
| `python_snippet` | — | — | **Inject Python code directly into the generated script.** **`code`**: multi-line string executed inside `async def run()`'s `try` block at the same level as `api_call`/`excel_write`/`word_write`; can access `page`, `CONFIG`, `load_workbook`, `Document`, etc. Use for **computed logic** (matching loops, data transforms) where `rows` cannot be statically provided at record time. **The code is executed immediately at record time** to validate dependencies, file existence, and logic — a runtime error during recording means the snippet is rejected before it enters the script. |
| `wait` | — | milliseconds | Wait |

> `extract_text` supports an optional **`"limit": N`** — only the first **N** matches.

> **Field label (shown in the file):** optional **`"field"`** or **`"field_name"`** (e.g. `"title"`, `"rating"`, `plot`). Output is formatted as **`【字段：{name}】`** + a separator line + body; if omitted, **`context`** is used as the label.

> **Multiple `extract_text` steps with the same `value` filename:** the generated script **writes** on first use, then **appends**; each block is labeled **`【字段：…】`**.

**Native `<select>` example (Sauce Demo `inventory.html` sort):** use `snapshot` to read the `<select>` `sel` and each `option` value. Price high → low is `hilo` — do **not** use `fill` or arrow keys to guess:

```json
{"action":"select_option","target":"[data-test=\"product-sort-container\"]","value":"hilo","context":"Sort by price high to low"}
```

### Scenario 1: quotes + news page + local brief (browser + API + file)

**Goal:** One workflow with **REST quote data**, a **browser news list**, and a **local brief** (`extract_text` and/or `api_call` **`save_response_to`**).

**User prompt checklist (when the flow includes `api_call`):** Ask the human (or infer from the API docs) for **base URL**, **required query/body fields**, **header names** if auth is header-based, and **which env var name** will hold each secret (e.g. `ALPHAVANTAGE_API_KEY`). **Key embedding strategy:** if the user supplied the real key → put it in the step's `"env"` field; the code generator writes it **directly into the script** (no `export` needed). If no key provided → use `__ENV:VAR__` placeholder only and tell the user to `export` before replay.

**Suggested order (adjust per site):**

1. **`api_call`** — fetch daily OHLCV (or any documented endpoint); save JSON for replay/offline use. Include `"env"` if key is available — key is embedded in script.
2. **`goto`** — open a finance news page (e.g. Yahoo Finance symbol page).
3. **Progressive probing** — `scroll` / `wait` / `snapshot` (and `dom_inspect` if needed) until a stable news selector exists.
4. **`extract_text`** — **scoped** selector + `limit`; reuse the same **`value`** filename to **append** sections with **`【字段：…】`**.

**`api_call` example A — key written directly into script (user supplied key in `###` block):**

```json
{
  "action": "api_call",
  "context": "Alpha Vantage daily OHLCV",
  "base_url": "https://www.alphavantage.co/query",
  "params": {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "outputsize": "compact",
    "datatype": "json",
    "apikey": "__ENV:ALPHAVANTAGE_API_KEY__"
  },
  "env": {"ALPHAVANTAGE_API_KEY": "user-supplied-real-key"},
  "method": "GET",
  "save_response_to": "ibm_time_series_daily.json"
}
```

Generated script contains `'apikey': 'user-supplied-real-key'` — runs directly, no `export` needed.

**`api_call` example B — key via env var (no key provided):**

```json
{
  "action": "api_call",
  "context": "Alpha Vantage daily OHLCV",
  "base_url": "https://www.alphavantage.co/query",
  "params": {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "outputsize": "compact",
    "datatype": "json",
    "apikey": "__ENV:ALPHAVANTAGE_API_KEY__"
  },
  "method": "GET",
  "save_response_to": "ibm_time_series_daily.json"
}
```

Generated script contains `'apikey': os.environ.get("ALPHAVANTAGE_API_KEY", "")` — requires `export ALPHAVANTAGE_API_KEY=…` before replay.

---

### Progressive probing (default; replaces “one snapshot is enough”)

**Use for:** SPAs, long pages, sites where the nav fills the first snapshot lines, and lists below the fold. **Core idea:** multiple rounds of **scroll → wait → snapshot (and `dom_inspect` if needed)**, then **`extract_text` with a scoped selector** — **never** use bare global `h3` / `a` for “headline list” style tasks.

**Why one snapshot is not “the whole page”:** the 📋 list is a **sample** (about 100 visible interactive nodes, ~20 section blocks) to cap tokens; **unrendered or unsampled regions** need **scroll + snapshot again** or **`dom_inspect`**.

**Standard flow (before extracting a block / list / titles):**

1. **`goto`** URL (SPA settle is built in).
2. Optional **`wait`** 500–2000 ms depending on the site.
3. **`scroll`** `value=800~1200` (or 1000–2000), **repeat 1–2 times** for below-the-fold and lazy load.
4. **`wait`** `value=600~2000` after scrolls.
5. **`snapshot`** — check 📋 / 🗂️ for the **target region** (list rows, block headings, containers with `data-testid`, etc.).
6. **If missing** — **`scroll`** again (~800px) and repeat 4–5; **if a parent looks right but children are unclear** — run **`dom_inspect`** on that container and derive `target` from children (`a`, `h3`, testids).
7. **`extract_text`:** `target` **must include a container prefix**, e.g. `"[data-testid=\"…\"] h3 a"`, `main h3`, `#nimbus-app …` (from snapshot / `dom_inspect`) — **do not** use a global `"h3"` alone for news-style headlines. Use **`limit`** for first N.

**Short recipe:**
```
goto → (scroll + wait) × 1–2 → snapshot → if no target, more scroll or dom_inspect → extract_text (scoped + limit)
```

> Lazy-load timing varies; if the target still does not appear, scroll ~800px, **`snapshot` again**, retry.

### Reading the `snapshot` output

`snapshot` returns two parts:

**1. `📋 Interactive elements`** — each line:
```
CSS selector  [placeholder=...]  「text preview」
```
- Use `sel` directly as the next `target`.
- If the element has no id/aria/testid, **the nearest parent** may be prepended, e.g. `[data-testid="news-panel"] h3`.

**2. `🗂️ Content blocks`** — each line:
```
[data-testid="block-id"]  ← heading 「Block title」
```
- To scope extraction, combine the block selector with a child selector:
  ```
  target = "[data-testid=\"target-block\"] h3 a"   ← only that block, not other sections
  ```
- Without `data-testid`, you can use Playwright text filters, e.g. `section:has(h2:text("Section title")) li`.

### Selector strength rules (extract_text target must follow)

**Bare tags (`h3`, `a`, `li`, …) are never unique** — they appear in navs, sidebars, footers, and modals. A selector must **combine multiple signals** to pin the real target.

**Ranked by strength. When building `target`, use at least one strategy above “bare tag”:**

| Priority | Strategy | Generic pattern | When to use |
|:--------:|----------|----------------|-------------|
| 1 | **`main` / `[role="main"]` + child** | `main h3`, `main article h3`, `[role="main"] li a` | Almost every modern site has `<main>`; simplest universal scope |
| 2 | **Snapshot block id / data-testid + child** | `#content h3`, `[data-testid="…"] li` | When snapshot 🗂️ shows a clear container |
| 3 | **Attribute filter** | `a[href*="/news/"]`, `li[class*="item"]` | Link paths with keywords, or list items with recognizable class fragments |
| 4 | **Semantic tag nesting** | `article h2`, `section ul > li`, `[role="list"] a` | No id / testid — rely on HTML5 semantic tags |
| 5 | **Text anchor (Playwright `:has`)** | `section:has(h2:text("…")) li` | Snapshot has a visible section heading but the container has no id |
| 6 | **Exclude noise** | `h3:not(nav h3):not(header h3)` | Fallback when none of the above work |
| **Banned** | **Bare tag** | ~~`h3`~~, ~~`a`~~, ~~`li`~~ | **Never** use alone; even the engine’s `main` fallback may still hit nav areas |

**Workflow (universal):**
1. Run **snapshot**; find the container holding target content in the 🗂️ block list (check heading / sel).
2. Container has `id` / `data-testid` → use **strategy 2**.
3. Container has no identifiers → check for `<main>` → use **strategy 1**.
4. Still unclear → run **`dom_inspect`** on the candidate container; derive **strategy 3–5** from children’s tag / class / href.
5. Compose, then `extract_text`.

**Recorder fallback:** If `target` is still a bare tag (letters only, no `#` `.` `[`, or space), the engine scopes to `<main>` / `[role="main"]` when present — but this is a **last resort**, not a substitute for the composite selectors above.

### Common scenarios

| Scenario | Suggested approach |
|----------|-------------------|
| Content blocks (news/list/comments) | scroll → wait → snapshot → pick selector from 🗂️ |
| Target not in snapshot | Not rendered or not sampled — scroll ~800px → snapshot again; or **`dom_inspect`** a likely parent |
| Repeating list/card rows | `extract_text` + `limit` for first N |
| “Load more” / expand | click → wait → snapshot → `extract_text` |

Example (navigate):
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{
  "action": "goto",
  "target": "https://example.com",
  "context": "Open target page"
}'
```

Example (fill search box; selector from snapshot):
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{
  "action": "fill",
  "target": "#search-input",
  "value": "keyword",
  "context": "Type keyword in search (selector from snapshot)"
}'
```

Example (extract list after scroll / lazy-load):
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{
  "action": "extract_text",
  "target": "[data-testid=\"content-list\"] h3 a",
  "value": "output.txt",
  "limit": 5,
  "field": "titles",
  "context": "First 5 titles (selector from snapshot block)"
}'
```

#### Step 4: Report to the user (fixed format)
```
✅ [Step N] {context}
📸 Screenshot: {screenshot_path} (browser state is visible on screen)
🔗 Current URL: {url}
Confirm this step, then reply **continue**, **1**, or **next** for the following step.
```

#### Step 5: On failure
- Explain the error to the user.
- Optionally `snapshot` again for fresh selectors and retry.
- **Do not record failed steps** (no `code_block` on failure — script stays clean).

---

### State transitions (check every message)

- **`end recording`** → **GENERATING**
- **`abort`** → run:
  ```bash
  python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-end --abort
  ```
  → back to **IDLE**
- **`continue`** / **`1`** / **`next`** / **`ok`** / **`y`** / **`go`** → continue the **current** multi-step plan step (see anti-timeout rules and shortcut confirmations above)

---

## GENERATING

Execute in order — **do not skip steps**:

1. Reply: "⏳ Saving and compiling recording…"

2. Run:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-end
   ```
   → Close browser → compile real steps into a full Playwright script → save `rpa/{filename}.py` → update registry

3. On success, print:
   ```
   ✨ RPA script generated! (from real recording; selectors verified in browser)

   📄 File: ~/.openclaw/workspace/skills/openclaw-rpa/rpa/{filename}.py
   📋 Recorded steps: {N}
   📸 Screenshots: ~/.openclaw/workspace/skills/openclaw-rpa/recorder_session/screenshots/

   Known limitations:
   • [If login was involved, remind user to log in before replay]
   • [Other caveats inferred from the recording; **do NOT** mention API keys or `export` commands — the generated script already checks for missing env vars at startup and prints instructions]

   To run this RPA later: if unsure what’s registered, send **`#rpa-list`** first to see **which recorded tasks are available**; then **`#rpa-run:{task name}`** (new chat) or **`run:{task name}`** (same chat).
   ```

4. **Do not LLM-rewrite the generated script** (agents must obey)
   - After successful `record-end`, `rpa/{filename}.py` is assembled by `recorder_server` `_build_final_script()` from real `code_block` segments — same source as `recorder_session/script_log.py`.
   - **Do not** generate a full replacement Playwright script from the task description alone; that drops recorder-validated selectors and `evaluate` semantics and often reintroduces `get_by_*` / `networkidle` patterns that diverge from the pipeline.
   - For behavior changes: **prefer** `record-start` and re-record the bad steps, then `record-end`; for tiny edits, patch **`rpa/*.py` locally** only, staying consistent with [playwright-templates.md](playwright-templates.md) (`CONFIG`, `_EXTRACT_JS`, `_wait_for_content`, `page.locator` + `page.evaluate`).

5. **Excel / Word — finalized layout**
   - **Primary path:** Use **`record-step`** **`excel_write`** / **`word_write`** during recording. After `record-end`, `recorder_server._build_final_script()` emits **one** `rpa/{filename}.py` with Office code **inside** `async def run()` (same `try` as Playwright / `api_call` / `merge_files`) and adds **top-level** `openpyxl` / `docx` imports when needed. **No** separate `rpa/*_office.py`.
   - **Fallback only:** If `task.json` flags Excel/Word but the recording has no `excel_write`/`word_write` steps, and the user gave explicit structure in chat, the agent may **append** supplemental code **only at the end** of that `.py` file — **never** replace recorder output.
   - **If details are missing:** do not invent business data; list required CONFIG / headers in the success message.

---

## RUN

Trigger: user message matches the **RUN** table above (`#rpa-run:` or `run:`); parsed `{task name}` is passed to `rpa_manager.py run` (**must match a registered name**; if unclear, user should **`#rpa-list`** first).

Meaning: **run an already-recorded script again** (repeat the same steps)—**not** start a new recording.

1. Reply: "▶️ Running 「{task name}」…"
2. Run:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py run "{task name}"
   ```
3. Capture stdout and summarize when done:
   ```
   ✅ Finished: 「{task name}」
   [stdout summary]
   ```
4. On error "task not found", list tasks:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py list
   ```

---

## LIST

Trigger: **order 2** above — the whole message is only `#rpa-list` (case-insensitive).

Meaning: answer **“which recorded RPA scripts can I use right now?”** — same output as `rpa_manager.py list` / `registry.json`.

1. Reply: "📋 Listing recorded RPA tasks you can run…"
2. Run:
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py list
   ```
3. Show **stdout** (light formatting OK); close with a short note that the names listed are **what’s available to run now**, and to execute one use **`#rpa-run:{task name}`** (new chat) or **`run:{task name}`** (this chat).

---

## Generated code quality (Recorder mode)

Because recording uses real CSS from a headed browser:

1. **Selectors are real** — every `target` comes from snapshot DOM, not guessed.
2. **Errors** — each step uses `try/except`, screenshot on failure, then re-raise.
3. **Paths** — outputs use `CONFIG["output_dir"]`.
4. **Portability** — generated `.py` runs standalone without OpenClaw.

---

## Recorder command log (audit: Playwright mapping per step)

- **During recording:** each `record-step` appends **one JSON line** (JSONL) to `recorder_session/playwright_commands.jsonl`.
- **Each line:** `command` (same JSON sent to the recorder: `action` / `target` / `value` / `seq`, …), `success`, `error`, `code_block` (Python fragment for the final RPA), `url`, `screenshot`.
- **Session bounds:** first line `type: session, event: start`; before successful `record-end`, append `event: end`, and copy the full log to `rpa/{task_slug}_playwright_commands.jsonl` for cross-check with `rpa/{task_slug}.py`.
- **`record-end --abort`:** deletes the whole `recorder_session` including the log.

---

## Example dialogue

```
User: #RPA
Agent: (ONBOARDING) … sign-up prompt…

User: Daily news scrape A
Agent: (deps-check A → record-start … --profile A) ✅ Chrome open…

User: Open example-news.com, search "AI", save the top 5 titles from the results to Desktop titles.txt
Agent:
  (multi-step: 3 sub-tasks → split)
  (plan-set '["Open site", "Search AI", "Save top 5 titles"]')
  (step 1 only: record-step goto) → screenshot
  📍 Progress: 1/3 done ✅ Open site
  📸 Screenshot: step_01_....png
  Reply continue / 1 / next for step 2/3: Search AI

User: 1
Agent:
  (plan-status → step 2)
  (record-step snapshot → find search input in 📋, e.g. input[name="q"])
  (record-step fill … AI)
  (record-step press Enter)
  (plan-next)
  📍 Progress: 2/3 done ✅ Search AI
  📸 Screenshot: step_03_....png
  Reply continue / 1 / next for step 3/3: Save top 5 titles

User: next
Agent:
  (plan-status → step 3)
  (record-step scroll value=1200 → lazy-load results)
  (record-step wait value=1200)
  (record-step snapshot → find results container in 🗂️ e.g. [data-testid="results"])
  (record-step extract_text [data-testid="results"] h3 a titles.txt limit=5)
  (plan-next → all done)
  🎉 All 3 steps done! titles.txt written to Desktop.
  Say "end recording" to generate the RPA script.

User: end recording
Agent: ✨ Generated: rpa/daily_news_scrape.py (5 steps, real recording, selectors verified)

User: #rpa-run:Daily news scrape
Agent: ▶️ Running… ✅ Finished.

User: run:Daily news scrape
Agent: ▶️ Running… ✅ Finished.

User: #rpa-list
Agent: 📋 Listing… (shows `rpa_manager.py list` output)
```

---

## Other resources

- Synthesis guidance: [synthesis-prompt.md](synthesis-prompt.md) (Recorder assembly vs legacy LLM synthesis; both must align with [playwright-templates.md](playwright-templates.md) / `recorder_server._build_final_script` — do not use old `get_by_role` + `networkidle` minimal skeletons as the main path)
- Playwright templates: [playwright-templates.md](playwright-templates.md) (same atoms as `recorder_server.py` `_build_final_script` / `_do_action`: `CONFIG`, `_EXTRACT_JS`, `_wait_for_content`, `page.locator` + `page.evaluate`)
- `rpa_manager.py` commands:

  **Plan (anti-timeout):**  
  `plan-set '<json>'` | `plan-next` | `plan-status`

  **Recorder (recommended):**  
  `record-start <task> [--profile A-N]` | `deps-check <A-N>` | `deps-install <A-N>` | `record-step '<json>'` | `record-status` | `record-end [--abort]`

  **General:**  
  `run <task>` | `list` (in chat, **`#rpa-list`** triggers LIST)

  **Legacy:**  
  `init <task>` | `add --proof <file> '<json>'` | `generate` | `status` | `reset`
