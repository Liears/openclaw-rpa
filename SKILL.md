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

Load one locale file and follow only that file.

## Locale Loading

1. Read `config.json` in this directory.
2. If it does not exist, read `config.example.json`.
3. Use the `locale` field to load exactly one file:
   - `zh-CN` -> `SKILL.zh-CN.md`
   - `en-US` -> `SKILL.en-US.md`

After loading the locale file, follow only that file for reply language, trigger handling, command mapping, workflow rules, and constraints.
