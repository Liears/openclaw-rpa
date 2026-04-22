---
name: openclaw-rpa
description: "Record browser, API, Excel, and Word tasks into replayable Python Playwright scripts. Use for #rpa, #rpa-api, #rpa-list, #rpa-run, and cookie-based login reuse via #rpa-login."
metadata:
  openclaw:
    emoji: "🤖"
    os: ["darwin", "linux"]
    localeConfig: "config.json"
    instructionFiles:
      zh-CN: "SKILL.zh-CN.md"
      en-US: "SKILL.en-US.md"
---

# openclaw-rpa

This skill is for recording deterministic RPA workflows and replaying them as standalone Python scripts under `rpa/`.

## What To Keep In Context

- Trigger detection for `#rpa`, `#rpa-api`, `#rpa-list`, `#rpa-run`, `#rpa-login`, `#rpa-login-done`, and `#rpa-autologin-list`
- Trigger detection for `#rpa-autologin <domain|url>` and `#rpa-help`
- Mapping user intent to `rpa_manager.py` commands
- The minimal recording workflow: confirm task, start recording, send small `record-step` actions, end with script generation
- Core constraints: keep steps small, avoid dumping large snapshots into chat, prefer deterministic actions

## Locale Loading

1. Read `config.json` in this directory.
2. If it does not exist, read `config.example.json`.
3. Use the `locale` field to load exactly one file:
   - `zh-CN` -> `SKILL.zh-CN.md`
   - `en-US` -> `SKILL.en-US.md`

After loading the locale file, follow that file for reply language, trigger handling, command mapping, and workflow rules.

## References

Load only when needed:

- `references/guide.zh-CN.md`
- `references/guide.en-US.md`
- `README.md`
- `README.zh-CN.md`
- `articles/`
