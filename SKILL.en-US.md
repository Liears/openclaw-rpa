---
name: openclaw-rpa
language: en-US
description: Record browser, API, Excel, and Word automation into replayable Python Playwright scripts. Use for `#rpa`, `#rpa-api`, `#rpa-list`, `#rpa-run`, and `#rpa-login` flows.
metadata: {"openclaw": {"emoji": "🤖", "os": ["darwin", "linux"]}}
---

# openclaw-rpa

Keep only the core protocol in context. Load `references/`, `README*`, and `articles/` only when more detail is required.

## When To Use

Use this skill when the user wants to:

- record a new RPA task
- run an existing recorded task
- list saved tasks
- save or reuse login cookies
- show available commands
- record mixed browser, API, Excel, and Word workflows

## Triggers

Match in this priority order:

1. `#rpa-run:<task>`
2. `#rpa-list`
3. `#rpa-autologin-list`
4. `#rpa-autologin <domain|url>`
5. `#rpa-login-done`
6. `#rpa-login <url>`
7. `#rpa-help`
8. `#rpa-api`
9. `#rpa` or `#RPA`

## Command Mapping

- List tasks: `python3 rpa_manager.py list`
- Run task: `python3 rpa_manager.py run "<task>"`
- Start recording: `python3 rpa_manager.py record-start "<task>" [--profile A-N] [--autologin <domain>]`
- Record one step: `python3 rpa_manager.py record-step '<json>'`
- Finish recording: `python3 rpa_manager.py record-end`
- Abort recording: `python3 rpa_manager.py record-end --abort`
- Check dependencies: `python3 rpa_manager.py deps-check <A-N>`
- Install dependencies: `python3 rpa_manager.py deps-install <A-N>`
- Start login capture: `python3 rpa_manager.py login-start <url>`
- Finish login capture: `python3 rpa_manager.py login-done`
- List saved login sessions: `python3 rpa_manager.py login-list`
- Show help: `python3 rpa_manager.py help`

## Minimal Workflow

1. Detect whether the user wants recording, replay, listing, or login-session management.
2. For new recordings, confirm task name and capability code first.
3. If the user first sends `#rpa-autologin <domain|url>`, check whether the matching cookie store exists; if it does, append `--autologin <domain>` to the next `record-start`.
4. Run `deps-check` when needed.
5. Start the recorder with `record-start`.
6. Decompose the task into small steps and advance only a small number of `record-step` actions per turn.
7. End with `record-end` to generate `rpa/<task>.py`.
8. For existing tasks, use `run` directly instead of re-recording.

## Login Session Handling

- `#rpa-login <url>`: open the login page, let the user complete login manually, then use `login-done` to export cookies.
- `#rpa-login-done`: save cookies from the current browser session.
- `#rpa-autologin-list`: list saved sessions.
- `#rpa-autologin <domain|url>`: this is skill-level state, not a standalone CLI command. It stores the target domain so the next `record-start` includes `--autologin <domain>`.
- If the cookie store does not exist, tell the user to run `#rpa-login <url>` first.

## Help

- For `#rpa-help`, call `python3 rpa_manager.py help` and return the result.

## Supported Actions

- Browser: `goto`, `click`, `fill`, `press`, `select_option`, `wait`, `scroll`, `snapshot`
- Extraction: `extract_text`, `extract_by_vision`
- Data and file operations: `api_call`, `merge_files`, `excel_write`, `word_write`, `python_snippet`

## Constraints

- Prefer deterministic, small actions.
- Do not paste full DOM snapshots or large JSON blobs back into chat.
- Prefer `extract_by_vision` when DOM extraction is unstable or the site is a heavy SPA.
- Generated outputs must remain standalone Python scripts.
- This skill is not for databases, heavy ETL, or system operations.

## On-Demand References

Read only if needed:

- `references/guide.en-US.md`
- `README.md`
- `articles/`
