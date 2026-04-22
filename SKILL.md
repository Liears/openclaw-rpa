---
name: openclaw-rpa
description: 录制浏览器、API、Excel、Word 自动化为可回放的 Python Playwright 脚本。用于 `#rpa`、`#rpa-api`、`#rpa-list`、`#rpa-run`、`#rpa-login` 等流程。
metadata:
  openclaw:
    emoji: "🤖"
    os: ["darwin", "linux"]
---

# openclaw-rpa

只保留中文核心协议。

## 触发词

按下列优先级匹配，先命中先执行：

1. `#rpa-run:{任务名}`
2. `#rpa-list`
3. `#rpa-autologin-list`
4. `#rpa-autologin <domain|url>`
5. `#rpa-login-done`
6. `#rpa-login <url>`
7. `#rpa-help`
8. `#rpa-api`
9. `#rpa` 或 `#RPA`

## 命令映射

- 查看任务：`python3 scripts/rpa_manager.py list`
- 运行任务：`python3 scripts/rpa_manager.py run "<任务名>"`
- 开始录制：`python3 scripts/rpa_manager.py record-start "<任务名>" [--profile A-N] [--autologin <domain>]`
- 录制步骤：`python3 scripts/rpa_manager.py record-step '<json>'`
- 结束录制：`python3 scripts/rpa_manager.py record-end`
- 放弃录制：`python3 scripts/rpa_manager.py record-end --abort`
- 检查依赖：`python3 scripts/rpa_manager.py deps-check <A-N>`
- 安装依赖：`python3 scripts/rpa_manager.py deps-install <A-N>`
- 开始登录态保存：`python3 scripts/rpa_manager.py login-start <url>`
- 完成登录态保存：`python3 scripts/rpa_manager.py login-done`
- 查看登录态：`python3 scripts/rpa_manager.py login-list`
- 查看帮助：`python3 scripts/rpa_manager.py help`

## 最小工作流

1. 识别用户是录制、运行、列出任务，还是管理登录态。
2. 若是新录制，先确认任务名与能力码。
3. 若用户先发了 `#rpa-autologin <domain|url>`，先检查对应 Cookie 是否存在；后续 `record-start` 追加 `--autologin <domain>`。
4. 需要时先执行 `deps-check`。
5. 用 `record-start` 建立录制会话。
6. 将任务拆成小步骤，每轮只推进少量 `record-step`。
7. 录制完成后执行 `record-end`，生成 `rpa/<task>.py`。
8. 运行已保存任务时，直接走 `run`，不要重新录制。

## 登录态处理

- `#rpa-login <url>`：打开登录页，等用户手动登录，再用 `login-done` 导出 Cookie。
- `#rpa-login-done`：保存当前浏览器 Cookie。
- `#rpa-autologin-list`：列出已保存会话。
- `#rpa-autologin <domain|url>`：这是 skill 级输入，不是单独 CLI 命令。它的作用是记录目标域名，并在下一次 `record-start` 时追加 `--autologin <domain>`。
- 若目标 Cookie 不存在，应提示用户先执行 `#rpa-login <url>`。

## 帮助

- `#rpa-help` 时，直接调用 `python3 scripts/rpa_manager.py help` 并返回结果。

## 支持动作

- 浏览器：`goto`、`click`、`fill`、`press`、`select_option`、`wait`、`scroll`、`snapshot`
- 提取：`extract_text`、`extract_by_vision`
- 数据与文件：`api_call`、`merge_files`、`excel_write`、`word_write`、`python_snippet`

## 约束

- 优先用确定性、小步的动作，不要一轮塞太多操作。
- 不要把完整 DOM snapshot 或大段 JSON 原样贴回对话。
- DOM 不稳定或页面是重型 SPA 时，优先考虑 `extract_by_vision`。
- 生成物必须保持为可独立运行的 Python 脚本。
- 这个 skill 不是数据库、重型 ETL、系统运维工具。
