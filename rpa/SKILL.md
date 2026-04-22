---
name: rpa
description: "Record browser actions once → replay as deterministic Python forever. Triggers: #rpa #RPA #rpa-api #rpa-login #rpa-autologin #rpa-list #rpa-run #rpa-help. Use when: user says RPA, 录制自动化, browser automation, or asks to automate browser/file tasks. Supports web clicks/fill/extract, Excel (.xlsx via openpyxl), Word (.docx via python-docx), HTTP API calls (httpx), and auto-login cookie reuse."
---

# rpa — Record → Replay RPA Compiler

一次录制 → 永久回放为确定性 Python 脚本，彻底告别重复任务中的"大模型税"。

## 触发词

| 你想… | 发什么 |
|--------|--------|
| **开始录制**新流程 | `#rpa`、`#RPA` |
| **录制含 API 接口** | `#rpa-api` |
| **查看已保存任务** | `#rpa-list` |
| **运行已保存任务** | `#rpa-run:{任务名}` |
| **保存网站登录态** | `#rpa-login <登录页URL>` |
| **查看已保存登录会话** | `#rpa-autologin-list` |
| **录制/回放时自动注入 Cookie** | 任务描述中加 `#rpa-autologin <域名或URL>` |
| **查看完整指令** | `#rpa-help` |
| **结束录制，生成脚本** | `#end`（录制中） |
| **放弃录制** | `#abort`（录制中） |

## 状态机

```
IDLE ──#rpa──► ONBOARDING ──任务名+能力码──► DEPS_CHECK
                                              │
                          ┌───────────────────┴───────────────────┐
                          ▼                                       ▼
                    RECORDING ◄──── #end / #abort ──── PLAN_EXEC
                          │
                          └─── 用户回复 continue/next ──► PLAN_EXEC
```

## 支持的动作（record-step）

| action | 说明 | 必需字段 |
|--------|------|---------|
| `goto` | 导航到 URL | `value`=URL |
| `click` | 点击元素 | `target`=CSS selector |
| `fill` | 填写输入框 | `target`, `value` |
| `select_option` | 下拉选择 | `target`, `value` |
| `press` | 按键 | `target`, `value` (key) |
| `scroll` | 滚动 | `value`=px |
| `wait` | 等待 | `value`=ms |
| `snapshot` | 获取 DOM 快照 | — |
| `extract_text` | 提取文本到文件 | `target`, `value`=文件名, `limit` |
| `api_call` | HTTP 请求 | `value`={method,url,headers,body,save_to} |
| `excel_write` | 写 Excel | `value`={path,sheets,headers,rows} |
| `word_write` | 写 Word | `value`={path,content} |
| `extract_by_vision` | 视觉识别提取 | `value`={prompt,output_file} |
| `python_snippet` | 注入 Python | `value`=Python 代码 |

## 登录态处理（#rpa-login）

```
#rpa-login https://passport.example.com/login  → 弹出浏览器
#rpa-login-done                                 → 导出 Cookie 到 ~/.openclaw/rpa/sessions/{domain}/cookies.json
```

回放/录制时任务描述加 `#rpa-autologin <domain>` 自动注入 Cookie。

## 依赖安装

能力码 `A-N` 对应不同功能：

| 码 | 依赖 |
|----|------|
| A | playwright, chromium |
| B | httpx |
| C | openpyxl |
| D | python-docx |
| E | 视觉模型（qwen/bedrock） |

```bash
python3 rpa/scripts/rpa_manager.py deps-check <能力码>
python3 rpa/scripts/rpa_manager.py deps-install <能力码>
```

## 运行已保存任务

```bash
python3 rpa/scripts/rpa_manager.py run "<任务名>"
# 或在对话中：
#rpa-run:<任务名>
```

## 查看所有任务

```bash
python3 rpa/scripts/rpa_manager.py list
# 或：#rpa-list
```

## 约束

- 生成脚本为普通 Python，可脱离 OpenClaw 独立运行
- 录制用真实 CSS 选择器，每步截图留证
- `extract_by_vision` 使用视觉模型从截图提取数据（用于 SPA）
- 不要用 `get_by_role` + `networkidle` 旧骨架作为主路径
- 重型 ETL / 数据库 / 大量 OS 自动化不在范围内

## 参考文件

- 代码模板：`rpa/references/playwright-templates.md`
- 合成原则：`rpa/references/synthesis-prompt.md`
- 示例脚本：`rpa/examples/`
