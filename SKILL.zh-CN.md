---
name: openclaw-rpa
description: 录制浏览器网站与本机文件操作；回放不调大模型—省费用、更快、少幻觉。github.com/laziobird/openclaw-rpa · #rpa-run #rpa-login #rpa-login-done #rpa-autologin #rpa-autologin-list #rpa-help #运行 #自动化机器人 #RPA。Use when user says #自动化机器人, #RPA, #rpa, #rpa-list, #rpa-login, #rpa-autologin, 录制自动化, browser automation, or asks to automate browser/file tasks.
metadata: {"openclaw": {"emoji": "🤖", "os": ["darwin", "linux"]}}
---

> **本文件语言：** `zh-CN`（由 [config.json](config.json) 或缺失时的 [config.example.json](config.example.json) 中 `locale` 选择；英文全文见 [SKILL.en-US.md](SKILL.en-US.md)）

> **GitHub 源码仓库：** **[https://github.com/laziobird/openclaw-rpa](https://github.com/laziobird/openclaw-rpa)**（安装说明、`rpa/` 示例、问题与反馈）

# openclaw-rpa

**典型场景示例（录制一次、反复回放；须遵守各站服务条款与所在地法规）：** 电商 **登录与购物** 全流程自动化；**典型场景 1**（见下）**行情 API + 新闻页 + 本地简报**；**Yahoo 财经** 仅浏览器侧行情与新闻；电影类网站 **一键汇总影评与评分**；**应付对账**（API **仅拉**待对账数据 + 本地 Excel 与发票核对 + **Word 表格**报告）详见 **[articles/scenario-ap-reconciliation.md](articles/scenario-ap-reconciliation.md)**。

## 这个 skill 做什么

**openclaw-rpa** 是一条 **录制 → 生成 Playwright 脚本 → 反复回放** 的流水线：在真实浏览器里按你的指令一步步执行并截图确认，**`#结束录制`** 后把步骤编译成 **`rpa/` 下的普通 Python**。日常**直接跑脚本**，不必每次让模型现场点网页。生成物可再按需加本机文件处理（`pathlib` / `extract_text` 等），见 [playwright-templates.md](playwright-templates.md)。

**亮点**

1. **大幅节约算力与费用** — 若每次重复操作都让**大模型**代点浏览器，单次会话往往 **数美金到数十美金** 量级（token、工具、长上下文等）。录成 RPA 后，**重复执行不再调大模型**，成本接近 **仅跑本地脚本**，且 **速度远快于** 每步都等模型推理。
2. **第一次把流程跑通、确认无误，以后按同一套步骤执行** — 录制阶段你已 **验证** 任务能正确完成；回放时 **严格按已保存步骤执行**（可预期、可重复），不必每次再让 AI「临场发挥」。避免 **反复调用大模型** 带来的 **稳定性变差** 与 **幻觉、误操作** 风险。

**推荐大模型：** Minimax 2.7 · Google Gemini Pro 3.0 及以上 · Claude Sonnet 4.6

**不适合** — 重型 ETL、数据库或大型运维；请用专门工具。

## 何时用（对照发什么）

| 你想… | 发什么 |
|--------|--------|
| **开始录制**新流程 | `#自动化机器人`、`#RPA`、`#rpa`，或提到 **Playwright automation** |
| **录制含 API 接口的流程** | `#rpa-api`（在消息里直接描述 API 或粘贴接口文档参数块 `###...###`） |
| **看已保存的任务** | `#rpa-list` |
| **执行已保存任务**（如新对话） | `#rpa-run:{任务名}` |
| **当前会话里执行** | `#运行:{任务名}` |
| **在 OpenClaw + 飞书等里定时/提醒** | 自然语言 + `#rpa-run:…`（以实际接入为准） |
| **保存网站登录态**（含验证码/短信/滑块） | `#rpa-login <登录页URL>` |
| **查看所有已保存的登录会话** | `#rpa-autologin-list` |
| **录制/回放时自动注入已保存 Cookie** | 任务描述中加 `#rpa-autologin <域名或URL>` |
| **查看完整指令列表与用法** | `#rpa-help` |

## 登录会话管理（#rpa-login / #rpa-autologin）

适用于需要短信验证码、滑块、扫码等**复杂登录**的网站（携程、微信、企业内网等）。核心思路：**只登录一次，Cookie 重复复用**。

### 三步完成登录会话保存

```
第 1 步：#rpa-login https://passport.ctrip.com/user/login
         → 弹出浏览器，跳转到该登录页

第 2 步：在浏览器里完成登录（账号/密码/短信/滑块，随便几步都行）

第 3 步：#rpa-login-done
         → 自动导出 Cookie，保存到 ~/.openclaw/rpa/sessions/passport.ctrip.com/cookies.json
         → 显示 Cookie 条数与参考过期时间
```

### 查看所有已保存的登录会话

```
#rpa-autologin-list
```

输出示例：
```
域名                             条数  会话型  保存时间               状态
─────────────────────────────────────────────────────────────────────────────────────────
passport.ctrip.com                 42      3  2026-04-07T10:23:15    🟢 28天后参考过期（2026-05-05）
accounts.google.com                18      8  2026-04-06T09:11:00    ⚠️  无固定过期时间（会话型）
```

### 录制/回放时自动注入 Cookie

在任务描述（或任务名称）中加入 `#rpa-autologin <域名或URL>`，系统会在启动录制/回放时自动找到对应 Cookie 文件并注入：

```
#rpa-autologin passport.ctrip.com
#rpa-autologin https://passport.ctrip.com/user/login
```

生成的 Python 脚本 `CONFIG` 里也会带上 `cookies_path`，直接可独立运行。

### Cookie 过期了怎么办？

Cookie 过期（或被服务端踢下线）时，脚本或录制里会被重定向回登录页。此时：
1. 重新执行 `#rpa-login <url>` → 手动登录 → `#rpa-login-done`，**覆盖旧文件**。
2. 再次录制/回放即可。

> 💡 **技术用户路径**：如果你有 Chrome DevTools 导出的 Cookie JSON（Playwright `add_cookies` 兼容格式），也可以直接将文件放到 `~/.openclaw/rpa/sessions/<域名>/cookies.json`，无需 `#rpa-login`。

### 查看所有可用指令 / View all commands

发送 `#rpa-help` 或执行：

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py help
```

输出完整指令参考表（中英双语），包含：登录会话管理、Recorder 录制、计划管理、通用命令、所有对话 `#` 指令及简单用法示例。

---

## 快速上手

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py list
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py run "任务名"
```

对话里可发 **`#rpa-list`** → **`#rpa-run:任务名`**，名称与 `registry.json` 一致即可。

### 运行已录制的任务（先看有哪些，再跑哪一个）

- **有哪些可以跑**：发 **`#rpa-list`**，列出 **当前已登记、可执行** 的任务名。不知道名字时**先发这一条**。
- **跑其中一个**：**`#rpa-run:任务名`**（**新开对话**）或 **`#运行:任务名`**（**当前会话**）。二者都是 **再次执行已生成脚本**，不是重新录制。

### 说明性例子（非穷举）

| 类型 | 含义 |
|------|------|
| **仅浏览器** | 如电商：**登录 → 选购 → 加购/结算**（参考仓库 `rpa/电商网站购物*.py`）；或 **Yahoo 财经** 行情/新闻；或电影站 **影评与评分** 汇总。 |
| **浏览器 + 文件** | 同上，必要时 **`extract_text`** 落盘。 |
| **浏览器 + HTTP API + 文件** | **典型场景 1**：**`api_call`**（如 [Alpha Vantage TIME_SERIES_DAILY](https://www.alphavantage.co/documentation/#daily)）写本地 JSON/文本，再配合 **`goto` + `extract_text`** 生成简报。 |
| **HTTP API + Excel + Word（可无网页）** | **应付对账案例**：Mock **GET** 拉批次、本地多 Sheet 对账、**不提交 ERP**；结果 **Word 表格**；见 **[articles/scenario-ap-reconciliation.md](articles/scenario-ap-reconciliation.md)**。 |
| **脚本内文件** | 录完后只加整理下载目录、改名等——可与网页无关。 |

## 推荐入门网站

**适合录制——结构稳定、开箱即用：**

| 类别 | 代表网站 |
|------|---------|
| **财经 / 数据** | Yahoo 财经（行情、新闻）、Google 财经、investing.com |
| **电商** | Sauce Demo（`saucedemo.com`）、AliExpress 商品页、eBay 搜索结果 |
| **新闻 / 媒体** | BBC News、Reuters、Hacker News、Reddit（列表页） |
| **参考资料** | Wikipedia、GitHub（公开仓库页、Issues 列表） |
| **招聘** | LinkedIn Jobs（公开搜索）、Indeed 结果页 |
| **出行 / 天气** | weather.com、Google Flights 结果页（只读） |
| **练习 / 测试站** | `the-internet.herokuapp.com`、`demoqa.com`、`automationpractice.pl` |

**不建议使用——容易失败或需要人工干预：**

| 场景 | 原因 |
|------|------|
| **高度动态的 SPA**（重度客户端路由、DOM 频繁变动） | 选择器在每次渲染间可能发生偏移；snapshot 可能遗漏未渲染内容 |
| **含验证码 / 反爬机制**（reCAPTCHA、hCaptcha、Cloudflare Turnstile） | 自动化会被拦截，须人工通过验证才能继续 |
| **登录后才可访问且无保存会话的流程** | 需手动处理账号密码与二次验证，回放前须先登录 |
| **无稳定 ID 的无限下拉流** | 渐进式探测有帮助，但结果可能不稳定 |

> **小贴士：** 尝试新网站时，建议先只做 `goto` + `snapshot`，确认页面结构可读后，再规划完整流程。

---

## 故障排查：`LLM request timed out`（与录制超时不同）

日志里若出现 `error=LLM request timed out`、`model=gemini-...`、`provider=google`：

| 含义 | 这是 **OpenClaw 对模型 API 的单次请求**（生成回复 + 工具规划）超过网关/客户端的 **LLM 超时**，不是 `record-step` 等待结果的 120s，也不是 Chromium 的导航超时。 |
| 常见诱因 | **单轮里想做的太多**：多步 `record-step`/长推理/把整页 snapshot 再抄进回复；上下文与输出过长；`gemini-3-pro-preview` 等模型推理 + 工具链较慢。 |
| Skill 侧 | **必须**遵守下方「防超时规则」：`plan-set` 拆解后 **每用户轮只推进一小步**（≤2 次 `record-step`），回复尽量短，勿在对话里重复粘贴完整 snapshot JSON。 |
| 环境侧 | 在 OpenClaw / Gateway 配置中 **调高 LLM 请求超时**（若产品提供该选项）；网络到 Google API 不稳定时也会拉长耗时。 |

---

## 触发检测

每次收到用户消息时，**按下表顺序**检查（**先命中先执行**，后续不再判断；⚠️ 顺序至关重要：所有以 `#rpa-` 开头的特殊指令必须在规则 9 之前命中，否则全部误判为 ONBOARDING）：

| 顺序 | 条件 | 进入状态 |
|:----:|------|---------|
| 1 | 消息为 **RUN**（见下表） | RUN |
| 2 | 消息**去掉首尾空白**后**等于** `#rpa-list`（不区分大小写，如 `#RPA-LIST`） | LIST |
| 3 | 消息**去掉首尾空白**后**等于** `#rpa-autologin-list`（不区分大小写） | AUTOLOGIN-LIST |
| 4 | 消息**去掉首尾空白**后以 `#rpa-autologin ` 开头（后跟域名或URL，不区分大小写） | AUTOLOGIN |
| 5 | 消息**去掉首尾空白**后**等于** `#rpa-login-done`（不区分大小写） | LOGIN-DONE |
| 6 | 消息**去掉首尾空白**后以 `#rpa-login ` 开头（后跟 URL，不区分大小写） | LOGIN |
| 7 | 消息**去掉首尾空白**后**等于** `#rpa-help`（不区分大小写） | HELP |
| 8 | 消息含 `#rpa-api`（不区分大小写） | RPA-API |
| 9 | 消息含 `#自动化机器人` 或 `#RPA` / `#rpa`（不区分大小写） | ONBOARDING |

**RUN 触发（命中顺序 1 即进入 RUN）：**

| 形式 | 说明 |
|------|------|
| `#rpa-run:{任务名}` | **在新对话里执行**（不依赖当前会话上下文）：消息**去掉首尾空白**后以 `#rpa-run:` 开头（**不区分大小写**，如 `#RPA-RUN:`）。**第一个英文冒号 `:` 之后**到**行尾**为 `{任务名}`（须与 `#rpa-list` 中某一项一致，首尾去空白）。 |
| `#运行:{任务名}` | **在当前会话里执行**：消息**去掉首尾空白**后以 `#运行:` 开头。**第一个英文冒号 `:` 之后**到**行尾**为任务名（同上，须为已登记任务）。 |

命中即拦截，不要直接执行原始任务。

---

## 状态机

```
IDLE ──触发词──► ONBOARDING（展示报名规则）
                    │
                    └──用户一条消息（「任务名 能力码」同行，或两行）──► DEPS_CHECK
                                                                          │
                    ┌─────────────────────────────────────────────────────┘
                    │  python3 rpa_manager.py deps-check <码>
                    ├─未通过 + 用户仅发「取消」（固定选项）──────────────────► IDLE（中止）
                    ├─未通过 + 用户「同意安装」──deps-install──再 deps-check──┐
                    └─已通过 ────────────────────────────────────────────────┤
                                                                               ▼
                                                                        RECORDING
RECORDING ──#结束录制──► GENERATING ──► IDLE
    │#放弃
    └──────────────────────────────────► IDLE
IDLE ──"#rpa-api"──► RPA-API ──解析完成──► （任务名+能力码规则同 ONBOARDING）──► DEPS_CHECK ──► RECORDING …
IDLE ──"#rpa-run:{任务名}" / "#运行:{任务名}"──► RUN ──► IDLE
IDLE ──"#rpa-list"──► LIST ──► IDLE
IDLE ──"#rpa-autologin-list"──► AUTOLOGIN-LIST ──► IDLE
IDLE ──"#rpa-autologin <域名|URL>"──► AUTOLOGIN ──► IDLE（记录 autologin_domain，下次 record-start 时注入）
IDLE ──"#rpa-login <URL>"──► LOGIN ──► IDLE（执行 login-start，等待用户手动登录）
IDLE ──"#rpa-login-done"──► LOGIN-DONE ──► IDLE（执行 login-done，导出 Cookie）
IDLE ──"#rpa-help"──► HELP ──► IDLE
```

> **说明：** 能力码 **B/C/F/N**（不含浏览器）时，`record-start` **不会**打开 Chrome，直接进入无浏览器录制模式。仅支持 **`api_call` / `merge_files` / `excel_write` / `word_write` / `python_snippet`** 等纯文件/API 步骤。

---

## AUTOLOGIN-LIST 状态

触发：消息**去掉首尾空白**后等于 `#rpa-autologin-list`。

执行：

```bash
python3 rpa_manager.py login-list
```

将输出结果直接展示给用户，回到 IDLE。

---

## AUTOLOGIN 状态

触发：消息以 `#rpa-autologin ` 开头，后跟域名或 URL。

提取规则：
- 取 `#rpa-autologin ` 之后的部分，去首尾空白，记为 `autologin_target`。
- 若 `autologin_target` 以 `http` 开头，用 `urlparse` 提取 hostname 并去掉 `www.` 前缀，得到 `autologin_domain`。
- 否则直接将 `autologin_target` 作为 `autologin_domain`。

执行步骤：
1. 检查 `~/.openclaw/rpa/sessions/{autologin_domain}/cookies.json` 是否存在。
   - **不存在** → 告知用户：「未找到 `{autologin_domain}` 的登录会话，请先发送 `#rpa-login <登录页URL>` 保存登录 Cookie。」回到 IDLE。
   - **存在** → 将 `autologin_domain` 保存到会话变量 `pending_autologin_domain`，回复：「✅ 已找到 `{autologin_domain}` 的登录 Cookie，下次录制或回放时将自动注入。现在可以开始任务：直接告诉我任务名称即可。」
2. 用户告知任务名后，进入正常 ONBOARDING → DEPS_CHECK → RECORDING 流程，但在 `record-start` 命令中追加 `--autologin {autologin_domain}`。

**`record-start` 带 autologin 时的完整命令：**

```bash
python3 rpa_manager.py record-start "任务名" --autologin passport.ctrip.com
```

---

## LOGIN 状态

触发：消息以 `#rpa-login ` 开头，后跟登录页 URL。

提取规则：取 `#rpa-login ` 之后的部分，去首尾空白，记为 `login_url`。

执行步骤：
1. 执行：`python3 rpa_manager.py login-start {login_url}`
2. 浏览器弹出后，回复用户：「✅ 登录浏览器已打开 → {login_url}。请在浏览器中完成登录（账号/密码/短信/滑块等），完成后发送 `#rpa-login-done`。」
3. 等待用户发送 `#rpa-login-done`，进入 LOGIN-DONE 状态。

---

## LOGIN-DONE 状态

触发：消息**去掉首尾空白**后等于 `#rpa-login-done`。

执行步骤：
1. 执行：`python3 rpa_manager.py login-done`
2. 展示命令输出（Cookie 条数、域名、参考过期时间）。
3. 回到 IDLE。

---

## HELP 状态

触发：消息**去掉首尾空白**后等于 `#rpa-help`。

执行步骤：
1. 执行：`python3 rpa_manager.py help`
2. 将输出完整展示给用户。
3. 回到 IDLE。

---

## RPA-API 状态

触发：消息含 **`#rpa-api`**（不区分大小写）。

### ⛔ 绝对禁止（Agent 必须遵守）

> **禁止直接调用 HTTP API、禁止自己运行任何 Python / httpx / requests / curl、禁止直接返回 API 响应内容。**  
> `#rpa-api` 的**唯一目标**是把 API 调用**录制成可独立回放的 RPA 脚本**（与 `#rpa`/`#自动化机器人` 的浏览器录制完全平行）。  
> 无论 API 多简单，都必须走 `record-start` → `record-step api_call` → `record-end` 流水线。  
> **擅自"帮用户直接取数据"即为违规。**

### 逐字输出以下引导语，不要省略

```
🤖 OpenClaw RPA 录制器已就绪（API + 浏览器模式）

我将把你的 API 调用和浏览器步骤录制成可重复执行的 RPA 脚本。
之后日常直接跑脚本——不需要每次让模型现场请求数据。

工作方式：
1. 我解析你提供的 API 信息 → 密钥直接写入生成脚本（无需额外 export）
2. 浏览器 / 文件步骤逐一在真实 Chrome 里执行并截图确认
3. 说"#结束录制" → 编译成完整 Playwright Python 脚本

请发送：任务名称 + 空格 + 能力码（例如：周报数据汇总 F）；两行格式亦可。
```

### 解析 `###...###` API 声明块

用户可在消息里用 `###` 包裹声明 API，支持两种写法：

**写法 A — 自然语言描述 + API 文档 URL + 密钥**
```
###
任务描述（如：拉取 NVDA 日线数据，保存到桌面的 nvda_time_series_daily.json）
对应的 API 文档  https://www.alphavantage.co/documentation/#daily
对应的 API key  YOUR_API_KEY
###
```

**写法 B — 直接粘贴 API 文档参数片段 + 密钥**
```
###
API Parameters
❚ Required: function    → TIME_SERIES_DAILY
❚ Required: symbol      → IBM
❚ Required: apikey
示例: https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
对应的 apikey  YOUR_API_KEY
###
```

两种写法可混用，块外的普通行是后续的**浏览器 / 文件步骤**。

### AI 处理步骤（按序执行，不允许跳过或合并）

**步骤 0 — 输出上方引导语并等待「任务名 + 能力码」**（格式与下方 **ONBOARDING** 相同：`任务名 能力码` 同行，或两行兼容；若用户在同一条消息里已写明，可直接进入 **DEPS_CHECK**）。

**步骤 1 — 提取块内 API 信息**  
   - 从 URL 或文档片段中识别：**base_url**、**必填 params**（function、symbol 等）、**密钥字段名**（apikey / token / key 等）  
   - 如果提供了文档 URL，从 URL 路径 + 参数推断 base_url 与 function；以用户描述补充 symbol 等业务参数  
   - 用户描述里的保存文件名 → **`save_response_to`** 字段

**步骤 2 — 把密钥写入脚本（用户已提供时）**  
   - 根据 API 来源**自动命名**变量名（Alpha Vantage → `ALPHAVANTAGE_API_KEY`；OpenAI → `OPENAI_API_KEY`；新浪 → `SINA_API_TOKEN`）  
   - 在 `record-step` JSON 中：
     - `params`（或 `headers`）里的密钥字段值使用 **`__ENV:变量名__`** 占位符  
     - **同时**将真实 key 放入本步的 **`"env"`** 字段：  
       ```json
       {
         "action": "api_call",
         ...,
         "params": {"apikey": "__ENV:ALPHAVANTAGE_API_KEY__", ...},
         "env": {"ALPHAVANTAGE_API_KEY": "用户提供的真实密钥"}
       }
       ```
   - 生成脚本时 `env` 里有真实值 → **密钥直接写入脚本**（如 `'apikey': 'UXZ3BOXOH817CQWS'`），**无需 `export`**，脚本可直接运行  
   - **不向用户输出** `export ...` 提示；用一句话确认"密钥已写入脚本，回放时无需额外配置"  
   - 若用户**未提供密钥**，则仅用占位符（不填 `env`），并告知用户运行前需 `export 变量名=…`

**步骤 3 — 收到「任务名 + 能力码」并完成 DEPS_CHECK 后立即开始录制**  
   - 执行 `record-start "{任务名}" --profile {能力码}`（能力码规则同 ONBOARDING；须先 `deps-check` 通过）  
   - 等 `✅ Recorder 已就绪` 后，将 `api_call` 步骤作为**第一步**注入（密钥已在 `env` 字段）：
     ```bash
     python3 rpa_manager.py record-step '{"action":"api_call","context":"...","base_url":"...","params":{...,"密钥字段":"__ENV:变量名__"},"env":{"变量名":"真实密钥"},"method":"GET","save_response_to":"..."}'
     ```
   - 向用户确认 api_call 执行结果（截图 / 文件已写入）

**步骤 4 — 继续处理块外的步骤**  
   按 RECORDING 状态的单步录制协议处理浏览器步骤、`merge_files` 等，直到用户发 `#结束录制`。

> **没有 `###` 块时**：若消息只有 `#rpa-api` 而无块，输出引导语，询问「任务名 + 能力码」（同行格式 `任务名 F` 或两行，规则同 ONBOARDING）→ **DEPS_CHECK** → **RECORDING**，用户在录制过程中手动下达 `api_call` 步骤即可。

## ONBOARDING 状态

**逐字输出下方引导语**（勿省略能力码表格与报名格式说明）：

```
🤖 OpenClaw RPA 实验室已就绪

在 AI 协助下，把你在常见网站上的操作、以及需要的本机文件步骤，录制成可反复执行的 RPA 脚本。
之后日常直接跑脚本即可，不必每次让模型现场点网页——省算力，步骤按录制执行，少受幻觉影响。

── 报名（一条消息搞定）──
格式：  任务名称  能力码
示例：  供应商对账入表 D

能力码（末尾一个大写字母）：
  A  只要网页（浏览器自动化）
  B  只要 Excel 表格（生成/编辑 .xlsx，不依赖本机是否安装 Microsoft Excel）
  C  只要 Word 文档（生成/编辑 .docx，不依赖本机是否安装 Microsoft Word）
  D  网页 + Excel
  E  网页 + Word
  F  Excel + Word（无网页步骤）
  G  网页 + Excel + Word
  N  以上都不需要（例如只做接口请求 + 合并文本文件等）

关于 Excel / Word（白话）：
• 一般能做：多工作表、写入数据、表头、列宽、冻结首行、隐藏列；Word 里按模板填空、段落、普通表格。
• 暂不适合：表格宏、数据透视刷新、复杂公式在「没开 Excel」时要当场算准；Word 修订模式、复杂公文域、老版 .doc。

依赖会装在你运行本 skill 时用的同一个 Python 环境里（与 Playwright 一致）。若缺少组件，我会请你确认后再安装。

工作方式（进入录制后）:
1. 下达指令 → 我在浏览器里真实执行（若任务包含网页），截图给你确认
2. 说"#结束录制" → 编译成 RPA 脚本

常用指令:
• 输入"#结束录制" → 生成可独立运行的 Playwright 脚本（含 Office 时见 GENERATING 增补规则）
• 输入"#放弃"     → 关闭浏览器，清空本次录制
• 多步任务拆成计划后，要进入下一步时可只发:**#继续**、**1** 或 **next**（与「#好」「#下一步」「ok」一样有效）
• 任务里需要调用 HTTP API？**新建对话**发送 **`#rpa-api`** 触发专用录制流程（`#rpa-api` 是 IDLE 触发词，不是录制中的步骤指令）。
• 查看帮助或所有可用指令：**`#rpa-help`**；查看已录制任务列表：**`#rpa-list`**（两者功能不同）。

推荐网站：Yahoo 财经、BBC News、Hacker News、GitHub 公开页、Wikipedia。
不建议：含验证码、短信的网站（reCAPTCHA / hCaptcha）

请发送：任务名称 + 空格 + 能力码（例如：供应商对账入表 F）
```

---

## DEPS_CHECK（依赖门控，在 ONBOARDING 用户报名之后）

**解析用户消息（支持同行与两行两种格式）**

1. **同行格式**（推荐）：整条消息去空白后，**末尾的单词**（空格分隔的最后一个 token）若为 `A`–`G` 或 `N`（大小写不限，统一大写）→ 能力码；**前面的内容** trim 后 → `{任务名}`。  
2. **两行格式**（兼容）：按行拆分（去掉首尾空行），最后一行为单字符能力码 → 能力码；此前所有行合并 → `{任务名}`。  
3. 两种格式均无法解析（找不到合法能力码）→ **不要** `record-start`；回复纠错示例 `供应商对账入表 F`，请用户重发。  
4. 若用户**在同一轮**触发词消息里已附带格式正确的内容（少见）→ 直接进入本流程，**不要**再索要任务名。

**检查（与 Playwright 同一 `python3`）**

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py deps-check {能力码}
```

- **退出码 0**：立即执行 **进入录制**（见下节 `record-start … --profile`）。  
- **非 0**：用**非技术话术**说明缺什么，并**逐字**提示用户：下面只有两个合法回复，**不要**加其它字或标点。

**固定选项（仅此两种，多一字都不算）**

对用户说明：请**整行只发下面二选一**（复制粘贴最稳妥）：

| 你选的回复（去掉首尾空白后须 **完全等于** 该字符串） | 含义 |
|------------------------------------------------------|------|
| `同意安装` | 执行 `deps-install`，再 `deps-check`，通过后 `record-start` |
| `取消` | 中止报名，回 IDLE，不安装 |

- 若用户发了**既不是** `同意安装`**也不是** `取消` 的内容（例如「好的」「ok」「安装吧」）→ **不要**执行 `deps-install`；回复一句：**请只回复 `同意安装`（四字）或 `取消`（二字），整行无其它内容。**  
- 用户发 `同意安装` →（尚未 `record-start` 则无浏览器可关）执行  
  `python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py deps-install {能力码}`  
  → 再 `deps-check` → 通过则 `record-start`；失败则贴 stderr，回 IDLE。  
- 用户发 `取消` → 回 IDLE。

> **须安装时**：仅当用户消息经去空白后**严格等于** `同意安装` 时，才允许执行 `deps-install`。

---

## RECORDING 状态（Recorder 模式 — 有界面真实录制）

### 进入录制（DEPS_CHECK 通过后）

执行（**必须带 `--profile`，与报名能力码一致**）：

```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-start "{任务名}" --profile {能力码}
```

等命令输出 `✅ Recorder 已就绪` 后，根据能力码回复以下之一：

**含浏览器（A / D / E / G）：**
```
✅ 已进入录制模式: 「{任务名}」
能力码已写入 recorder_session/task.json（needs_excel / needs_word / needs_browser / capability）。
🖥️  Chrome 窗口已打开，请发送指令，我将在真实浏览器中执行并截图确认。
请下达指令，为你拆解任务
```

**不含浏览器（B / C / F / N）：**
```
✅ 已进入录制模式: 「{任务名}」
能力码已写入 recorder_session/task.json（needs_excel / needs_word / needs_browser / capability）。
📂 无浏览器模式——本任务仅支持文件 / API 操作，可使用 `excel_write`、`word_write`、`api_call`、`python_snippet`、`merge_files` 等步骤。
请下达指令
```

---

### ⚡ 防超时规则：多步指令必须拆解，每轮只执行一步

**判断标准：** 用户指令中包含 2 个以上可独立完成的原子操作（导航、搜索、点击、提取等）时，触发拆解流程。

#### 拆解流程

**第一轮（收到多步指令时）：**

1. 将指令分解为原子子任务列表（每个子任务对应 ≤2 次 record-step 调用）
2. 调用 `plan-set` 持久化计划：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py plan-set '["子任务1描述", "子任务2描述", "子任务3描述"]'
   ```
3. 执行 **第 1 步**（仅此一步，不继续）
4. 固定结尾：
   ```
   📍 进度: 1/{N} 步已完成
   ✅ [步骤描述]
   📸 截图: {path}
   请确认截图，然后说「#继续」或「1」或「next」执行第 2/{N} 步（见下方快捷确认词）。
   ```

> **快捷确认词（均视为「继续执行下一步」）：** `#继续`、`1`、`next`、`#好`、`#下一步`、`ok`（`next` 不区分大小写）。用户只打 **`1`** 或 **`next`** 即可，无需完整句子。

**后续轮（收到上述快捷确认词之一时）：**

1. 查看当前计划进度：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py plan-status
   ```
2. 执行当前步对应的操作（snapshot + action，≤2 次 record-step）
3. 推进计划：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py plan-next
   ```
4. 若还有下一步 → 输出进度，等待用户确认；若全部完成 → 输出：
   ```
   🎉 所有 {N} 步已全部完成！
   可以说「#结束录制」生成 RPA 脚本，或继续描述更多操作。
   ```

> **为什么这么设计：** 每次 LLM 请求只运行 2-3 个工具调用；单步 `record-step` 等待录制器回写结果最多 **120s**（与 `rpa_manager` 轮询一致），仍须拆解多步以免总耗时长触发 "LLM request timed out"。

---

### 单步录制协议（每条用户指令执行以下流程）

#### 第一步：获取当前页面元素（免费，不记入脚本）
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{"action":"snapshot"}'
```
→ 返回页面中所有可交互元素及其 **真实 CSS 选择器**（如 `#search-input`、`input[name="q"]`、`[aria-label="搜索"]`）。

#### 第二步：根据 snapshot 确定目标元素的 CSS 选择器
- **必须使用 snapshot 中返回的真实 `sel` 字段**，禁止凭空猜测。
- **默认用「渐进式探测」**（见下节）：不要指望单次 snapshot 覆盖全页；目标未出现就 **scroll → wait → snapshot** 循环，必要时 **`dom_inspect`**。
- 若 snapshot 未返回有效选择器，说明目标元素可能在页面下方未渲染，先 `scroll` 再重新 snapshot。

#### 第三步：执行操作（以下任选）

| action | target | value | 说明 |
|--------|--------|-------|------|
| `goto` | URL 字符串 | — | 导航到页面，wait_until=domcontentloaded + 1.5s SPA 等待 |
| `snapshot` | — | — | 获取当前 DOM 元素 + 内容区块（不记入脚本） |
| `fill` | CSS 选择器 | 填写文本 | **仅用于 `<input>` / `<textarea>`**；**不要**对原生 `<select>` 用 fill |
| `select_option` | `<select>` 的 CSS | **option 的 value** 或见下 | 原生下拉框：`locator.select_option(...)`。可选 `"select_by": "label"` 时 `value` 填可见文字；`"index"` 时填数字下标 |
| `press` | 键名（如 `Enter`） | — | 按键并等待页面稳定 |
| `click` | CSS 选择器 | — | 点击并等待页面稳定 |
| `scroll` | — | 像素数 | 向下滚动 N 像素 |
| `scroll_to` | CSS 选择器 | — | **滚动到指定元素，触发懒加载**，再 wait + snapshot |
| `dom_inspect` | 容器 CSS 选择器 | — | **调试**：列出容器内子元素结构（**不记入脚本**），用于反推列表/标题的真实选择器 |
| `extract_text` | CSS 选择器 | 输出文件名 | 提取多元素文本 → 写到 ~/Desktop/文件名 |
| `api_call` | — | — | **HTTP 调用**（与当前页无关）：二选一 **`url`** 完整地址，或 **`base_url` + `params`** 拼查询串。可选 **`method`**（默认 `GET`）、**`headers`**、**`body`**（POST JSON）、**`save_response_to`**（相对文件名 → 写入 ~/Desktop）。**密钥占位符：** 在 **`params` / `headers` 的字符串值** 中使用 **`__ENV:环境变量名__`**（例如 `"apikey": "__ENV:ALPHAVANTAGE_API_KEY__"`）。**若同时提供 `env` 字段**（如 `{"ALPHAVANTAGE_API_KEY":"真实密钥"}`），密钥将**直接写入生成脚本**，运行时无需 `export`；省略 `env` 则生成 `os.environ.get("变量名", "")`，需手动 `export`。 |
| `merge_files` | — | — | **桌面文件合并**（纯本地操作，不涉及浏览器）：**`sources`**（文件名列表，均在 ~/Desktop 下）、**`target`**（目标文件名）、可选 **`separator`**（分隔符，默认 `"\n\n"`）。典型用途：把 `api_call` 保存的 JSON 与 `extract_text` 保存的新闻文本合并成一份简报。 |
| `excel_write` | — | — | **写入 Excel .xlsx**（依赖 openpyxl；**无需安装 Microsoft Excel**）。**`path`** 或 **`value`**：相对文件名（录制时落 **~/Desktop**，生成脚本用 `CONFIG["output_dir"]`）。**`sheet`**：工作表名。**`headers`**：可选，表头字符串数组。**数据行三选一**：① **`rows`**：二维数组，静态数据行；② **`rows_from_json`**：`{"file":"x.json","outer_key":"batches","inner_key":"lines","fields":["f1","f2"],"parent_fields":["batch_id"]}` — 从 Desktop JSON 动态展平嵌套数组（`inner_key`/`parent_fields` 可省略）；③ **`rows_from_excel`**：`{"file":"发票导入_本周.xlsx","sheet":"发票侧","skip_header":true}` — 从另一 xlsx 的指定 sheet 复制数据行。**`freeze_panes`**：可选，如 `"A2"` 冻结首行。**`hidden_columns`**：可选，要隐藏的 **列号（从 1 起）** 列表，如 `[1]` 隐藏 A 列。**`replace_sheet`**：默认 `true`（删除同名表后重建）；`false` 时在已存在表**末尾追加** `rows`。 |
| `word_write` | — | — | **写入 Word .docx**（依赖 python-docx；**无需安装 Word**）。**`path`** 或 **`value`**：相对文件名。**`paragraphs`**：字符串数组，每个元素一个新段落。**`table`**：可选，`{"headers": [...], "rows": [[...]]}` — 在段落之后插入一张表格（自动应用 "Table Grid" 样式）。**`mode`**：`new`（默认，新建或覆盖）或 `append`（已存在则尾部追加）。 |
| `python_snippet` | — | — | **通用兜底 action**：当所需操作没有对应的专用 action（`api_call` / `excel_write` / `word_write` / 浏览器类）时，由 AI 生成完整 Python 代码并注入。**`code`**：多行字符串，**录制时立即执行验证**（依赖缺失 → 提示 `deps-install`；文件不存在 → 提示前序步骤；语法/运行时错误 → 返回 traceback）；验证通过后写入 `code_block`，之后每次回放在 `run()` 的 `try` 块内执行。**AI 生成 `code` 时必须遵守下方「执行环境」约束。** |
| `wait` | — | 毫秒数 | 等待 |

> `extract_text` 支持额外的 `"limit": N` 字段，只取前 N 条。

---

### `python_snippet` 执行环境（AI 生成代码时的约束）

> 完整设计原理、验证机制、可用符号表及 AP 对账案例示例见 **[articles/python-snippet-design.md](articles/python-snippet-design.md)**。

> **设计原则**：已有专用 action 的操作**必须**用专用 action；只有专用 action 无法覆盖的逻辑（计算、多源聚合、自定义格式化等）才使用 `python_snippet`。

**录制时 & 回放时可用的符号：**

| 符号 | 类型 | 说明 |
|------|------|------|
| `CONFIG["output_dir"]` | `Path` | 输出目录（录制时为 `~/Desktop`，回放时按配置）；**所有文件路径必须通过此前缀构造** |
| `CONFIG["task_name"]` | `str` | 任务名 |
| `Path` | `pathlib.Path` | 路径操作 |
| `json` | module | 标准库 json |
| `os` | module | 标准库 os |
| `re` | module | 标准库 re |
| `datetime` | module | 标准库 datetime |
| `load_workbook` | openpyxl | 读已有 xlsx（需能力 B/F）|
| `Workbook` | openpyxl | 新建 xlsx |
| `get_column_letter` | openpyxl | 列号转字母 |
| `Document` | python-docx | 读写 docx（需能力 C/F）|
| `page` | Playwright Page | 浏览器页对象；纯文件步骤值为 `None`，**不可在非浏览器步骤中调用** |

**AI 生成代码的检查清单（每次生成前必须过一遍）：**

1. 所有文件路径用 `CONFIG["output_dir"] / "文件名"` 构造，**禁止硬编码 `~/Desktop`**
2. 引用了 `load_workbook` / `Workbook` → 确认任务能力码包含 B 或 F
3. 引用了 `Document` → 确认任务能力码包含 C 或 F
4. 读取前序步骤生成的文件（如 `reconcile_raw.json`）→ 在代码前加 `assert` 或 `if not ... .exists(): raise FileNotFoundError(...)`，让录制时验证即时失败并给出明确提示
5. 不使用任何未在上表列出的第三方库（如 pandas、numpy）；若必须使用，先用 `pip install` 安装并在 SKILL `requirements.txt` 中记录

> **字段名（写入文件时显示）：** 可选 `"field"` 或 `"field_name"`（如 `"片名"`、`"rating"`、`plot`）。输出排版为 `【字段：{名称}】` + 分隔线 + 正文；未填时沿用 `context`。

> **同一 `value` 文件名多次 `extract_text`：** 生成脚本会**自动**处理：该文件名**第一次** `write_text`，**后续**同文件名**追加**；每段均带 `【字段：…】` 标识。

**原生 `<select>` 示例（Sauce Demo `inventory.html` 排序）：** 用 `snapshot` 看 `<select>` 的 `sel`，`option` 的 value。价格从高到低为 `hilo`，不要用 `fill` / 箭头键硬猜：

```json
{"action":"select_option","target":"[data-test=\"product-sort-container\"]","value":"hilo","context":"按价格从高到低排序"}
```

### 典型场景 1：行情 + 新闻页 + 本地简报（浏览器 + API + 文件）

**目标：** 同一任务里既有 **REST 行情数据**，又有 **浏览器里新闻列表**，再 **合并进一份本地简报**（`extract_text` 与/或 `api_call` 的 `save_response_to`）。

**用户提示词 / 助手侧清单（流程含 `api_call` 时）：** 向用户确认或根据 API 文档推断 **接口 base URL**、**必填查询/Body 字段**、**若鉴权在 Header 则 Header 名**，以及 **每个密钥对应的变量名**（如 `ALPHAVANTAGE_API_KEY`）。**密钥写入策略：** 用户在 `###` 块中已提供真实 key → 放入 `record-step` 的 `"env"` 字段，生成脚本时密钥**直接写入脚本**，无需 `export`；未提供 key → 用 `__ENV:变量名__` 占位，回放前需手动 `export`。

**推荐顺序（可按站点调整）：**

1. **`api_call`** — 拉取日线 OHLCV（或任意文档化接口），落盘便于回放脚本离线对照或二次处理。密钥已在 `env` 字段提供时，直接写入脚本；否则用 `__ENV:变量名__` 占位。
2. **`goto`** — 打开财经站新闻/行情页（如 Yahoo Finance 标的页）。
3. **渐进式探测** — `scroll` / `wait` / `snapshot`（必要时 `dom_inspect`），直到新闻列表选择器可靠。
4. **`extract_text`** — 带**容器前缀**的选择器 + `limit`，写入 **`value`** 为同一简报文件名（多段会**自动追加**，并带 `【字段：…】`）。

**`api_call` 示例 A — 密钥直接写入脚本（用户在 `###` 块提供了真实 key）：**

```json
{
  "action": "api_call",
  "context": "Alpha Vantage 日线行情",
  "base_url": "https://www.alphavantage.co/query",
  "params": {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "outputsize": "compact",
    "datatype": "json",
    "apikey": "__ENV:ALPHAVANTAGE_API_KEY__"
  },
  "env": {"ALPHAVANTAGE_API_KEY": "用户提供的真实密钥"},
  "method": "GET",
  "save_response_to": "ibm_time_series_daily.json"
}
```

生成脚本中的对应行变为：`'apikey': '用户提供的真实密钥'`（直接可运行，无需 `export`）。

**`api_call` 示例 B — 密钥通过环境变量引用（用户未提供 key，仅用占位符）：**

```json
{
  "action": "api_call",
  "context": "Alpha Vantage 日线行情",
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

生成脚本中的对应行变为：`'apikey': os.environ.get("ALPHAVANTAGE_API_KEY", "")`，回放前需 `export ALPHAVANTAGE_API_KEY=…`。

---

### 渐进式探测（默认策略；替代「单次 snapshot 定终身」）

**适用：** 所有 SPA、长页面、顶栏/导航占满 snapshot 前几条、以及「列表在首屏以下」的场景。**核心：** 多轮 **滚动 → 等待 → snapshot（必要时 dom_inspect）**，再 **带容器前缀** 做 `extract_text`；**不要**用裸 `h3` / `a` 等全局标签当标题列表。

**为何不能指望一次 snapshot「看见全页」：** 录制器返回的 📋 列表是**采样**（可见交互元素约 100 条、区块约 20 个），用于控 token；**不代表**页面只有这些节点。下方未渲染或未被采样的区域，要靠 **scroll + 再 snapshot** 或 **dom_inspect** 补。

**标准流程（提取某区块 / 列表 / 标题前必走）：**

1. **`goto`** 目标 URL（含 SPA settle，已内置）。
2. **`wait`** 可选：500–2000ms，视站点而定。
3. **`scroll`** `value=800~1200`（或 1000~2000），**重复 1～2 次**，触发 below-the-fold 与懒加载。
4. 每次滚动后 **`wait`** `value=600~2000`。
5. **`snapshot`** → 在 📋 / 🗂️ 中查找是否出现**目标区域**（列表项、区块标题、含 `data-testid` 的容器等）。
6. **若没有** → 继续 **`scroll`**（例如再 800px）并回到步骤 4～5；**若已有可疑父容器但子结构不清** → 对该容器做一次 **`dom_inspect`**，从子元素反推 `target`（如 `a`、`h3`、带 testid 的节点）。
7. **`extract_text`**：`target` **必须带容器前缀**，例如 `"[data-testid=\"…\"] h3 a"`、`main h3`、`#nimbus-app …`（以 snapshot/dom_inspect 为准）；**禁止**单独使用全局 `"h3"` 抽「新闻标题」类需求。配合 **`limit`** 取前 N 条。

**简写版（与上表一致）：**
```
goto → (scroll + wait) × 1～2 → snapshot → 目标未出现则再 scroll 或 dom_inspect → extract_text（带容器前缀 + limit）
```

> 每个 SPA 懒加载时机不同；若 snapshot 仍无目标，继续 **scroll ~800px** 后再 **snapshot** 重试。

### 🔍 读取 snapshot 结果的方法

`snapshot` 返回两部分信息：

**1. `📋 页面可交互元素`** — 每行格式：
```
CSS选择器  [placeholder=...]  「文本预览」
```
- 直接把 `sel` 用作下一步的 `target`
- 若元素本身无 id/aria/testid，会**自动向上查找最近父容器**补全，如 `[data-testid="news-panel"] h3`

**2. `🗂️ 页面内容区块`** — 每行格式：
```
[data-testid="区块名"]  ← 含标题「区块标题」
```
- 提取特定区块内容时，先用区块 selector 限定范围，再加子元素类型：
  ```
  target = "[data-testid=\"目标区块\"] h3 a"  ← 只抓该区块，不误抓其他版块内容
  ```
- 如果区块没有 data-testid，可用 `section:has(h2:text("区块标题")) li` 这类 Playwright 文本过滤语法

### 选择器强度规则（extract_text 的 target 必须遵守）

**裸标签（`h3`、`a`、`li`…）在任何页面上都不唯一**——它们在导航栏、侧栏、页脚、弹窗里都会出现。选择器必须**组合多个线索**才能钉住真正的目标。

**强度从高到低排列。构造 `target` 时，至少选用一种高于「裸标签」的策略：**

| 优先级 | 策略 | 通用写法 | 何时用 |
|:------:|------|----------|--------|
| 1 | **`main` / `[role="main"]` + 子标签** | `main h3`、`main article h3`、`[role="main"] li a` | 几乎所有现代站都有 `<main>`；最简单也最通用的圈定方式 |
| 2 | **snapshot 区块 id / data-testid + 子标签** | `#content h3`、`[data-testid="…"] li` | snapshot 🗂️ 里出现了明确容器时直接用 |
| 3 | **属性过滤** | `a[href*="/news/"]`、`li[class*="item"]` | 链接路径含关键词、或列表项有可识别 class 片段 |
| 4 | **语义标签嵌套** | `article h2`、`section ul > li`、`[role="list"] a` | 无 id / testid 时，靠 HTML5 语义标签限定 |
| 5 | **文本锚点（Playwright `:has`）** | `section:has(h2:text("…")) li` | snapshot 中有可见分区标题，但容器无 id 时 |
| 6 | **排除噪声区** | `h3:not(nav h3):not(header h3)` | 上述策略都不好用时的降级手段 |
| **禁止** | **裸标签** | ~~`h3`~~、~~`a`~~、~~`li`~~ | **永远不要**单独使用；即使引擎对裸标签有 `main` 防呆，仍可能落到导航区 |

**构造流程（通用）：**
1. 做 **snapshot**，在 🗂️ 区块列表中找**包含目标内容**的容器（看 heading / sel）。
2. 若容器有 `id` / `data-testid` → 直接用 **策略 2**。
3. 若容器无特征 → 看页面是否有 `<main>` → 用 **策略 1**。
4. 仍不确定 → 对候选容器执行 **`dom_inspect`**，从子节点的 tag / class / href 特征中取 **策略 3–5**。
5. 组合后再 `extract_text`。

**录制器防呆：** 若 `target` 仍为裸标签（仅字母、无 `#` `.` `[` 空格），引擎在存在 `<main>` / `[role="main"]` 时会自动限定搜索范围——但这是**最后兜底**，不能替代上述组合选择器。

### 💡 常见场景提示

| 场景 | 推荐做法 |
|------|---------|
| 页面内容区块（新闻/列表/评论等） | scroll 下去 → wait → snapshot → 从 🗂️ 区块找选择器 |
| snapshot 找不到目标元素 | 未渲染或未被采样：继续 scroll 800px → 再 snapshot；或对可疑父容器 **dom_inspect** |
| 提取重复结构内容（列表/卡片） | 用 `extract_text` + `limit` 只取前 N 条 |
| 需要点击展开更多内容 | click "更多" 按钮 → wait → snapshot → extract_text |

示例（导航到任意页面）：
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{
  "action": "goto",
  "target": "https://example.com",
  "context": "打开目标页面"
}'
```

示例（填写搜索框，selector 来自 snapshot）：
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{
  "action": "fill",
  "target": "#search-input",
  "value": "关键词",
  "context": "在搜索框输入关键词（selector 来自 snapshot）"
}'
```

示例（滚动触发懒加载后提取列表）：
```bash
python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-step '{
  "action": "extract_text",
  "target": "[data-testid=\"content-list\"] h3 a",
  "value": "output.txt",
  "limit": 5,
  "field": "标题",
  "context": "提取前 5 条内容标题（selector 来自 snapshot 区块）"
}'
```

#### 第四步：向用户汇报（固定格式）
```
✅ [步骤 N] {context}
📸 截图: {screenshot_path}（可在屏幕上直接看到浏览器变化）
🔗 当前 URL: {url}
请确认操作是否符合预期，然后回复「#继续」「1」或「next」进入下一步。
```

#### 第五步：若操作失败
- 向用户说明错误信息
- 可再次 snapshot 获取最新选择器后重试
- **不要记录失败步骤**（失败时无 code_block，不影响脚本）

---

### 状态转换检测（每条消息都检查）

- 收到 `#结束录制` → 进入 **GENERATING**
- 收到 `#放弃` → 执行：
  ```bash
  python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-end --abort
  ```
  → 回到 IDLE
- 收到 `#继续` / `1` / `next` / `#好` / `#下一步` / `ok` → 继续执行多步计划的**当前步骤**（见上方「防超时规则」与「快捷确认词」）

---

## GENERATING 状态

按序执行，**不要跳过任何步骤**：

1. 回复："⏳ 正在保存并编译录制步骤，请稍候…"

2. 执行：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py record-end
   ```
   → 关闭浏览器 → 将录制的真实操作步骤编译为完整 Playwright 脚本 → 保存到 `rpa/{filename}.py` → 更新 registry

3. 输出成功提示：
   ```
   ✨ RPA 脚本生成成功！（基于真实录制，选择器均经过浏览器验证）
   
   📄 文件: ~/.openclaw/workspace/skills/openclaw-rpa/rpa/{filename}.py
   📋 共录制 {N} 个步骤
   📸 截图目录: ~/.openclaw/workspace/skills/openclaw-rpa/recorder_session/screenshots/
   
   已知限制:
   • [如涉及登录，提醒用户手动登录后再运行]
   • [其他从录制内容识别出的注意事项；**不要**提及 API 密钥或 export 命令——脚本启动时已自动检查并提示]
   
   以后执行这个 RPA：不确定有哪些任务时先发 **`#rpa-list`** 查看 **当前可用的已录制任务**；再发 **`#rpa-run:{任务名}`**（新开对话）或 **`#运行:{任务名}`**（仍在本对话）。
   ```

4. **禁止用 LLM 全文重写已生成脚本**（Agent 必须遵守）  
   - `record-end` 成功后，`rpa/{filename}.py` 已由 `recorder_server` 的 `_build_final_script()` 从真实录制的 `code_block` **逐段拼装**，与 `recorder_session/script_log.py` 同源。  
   - **不要**根据「任务描述」再生成一份完整 Playwright 脚本去覆盖或替代上述文件；那会丢掉录制器保证的选择器与 `evaluate` 语义，且易重新引入 `get_by_*` / `networkidle` 等与流水线不一致的写法。  
   - 若用户要改行为：**优先**用 `record-start` 重录有问题的步骤后再次 `record-end`；仅当改动极小时，可在现有 `rpa/*.py` 上**局部**修改，且须与 [playwright-templates.md](playwright-templates.md) 中骨架、`_EXTRACT_JS`、`_wait_for_content` 风格一致。

5. **Excel / Word 与生成脚本结构（已定稿）**  
   - **主路径（推荐）**：录制阶段通过 **`record-step` 的 `excel_write` / `word_write`** 完成 Office 操作；`record-end` 后代码已由 `recorder_server._build_final_script()` **与 Playwright 步骤写入同一 `rpa/{filename}.py`**（在 `async def run()` 的 `try` 块内，与 `api_call`、`merge_files` 同级），顶部按需注入 `openpyxl` / `docx` 的 import。**不再**单独维护 `rpa/*_office.py`。  
   - **兜底（仅当未录到 Office 步骤）**：若 `task.json` 中 `needs_excel` / `needs_word` 为 `true` 但录制 JSONL 中无 `excel_write`/`word_write`，且用户在对话里已明确表结构/路径，允许 Agent 在 `record-end` 成功后 **仅向该 `.py` 文件末尾追加** 补充函数或 `main` 调用，**不得删除或改写**录制器已生成的段落。  
   - **若信息不足**：不要编造业务数据；在成功提示中列出待补 CONFIG/表头。

---

## RUN 状态

触发：用户消息满足上表 **`#rpa-run:`** 或 **`#运行:`** 规则；解析出的 `{任务名}` 传入 `rpa_manager.py run`（**须与已登记任务名一致**；不确定时让用户先 **`#rpa-list`**）。

含义：**执行一条已录制好的 RPA 脚本**（再次跑同一套步骤），不是开始新录制。

1. 回复："▶️ 正在运行「{任务名}」…"
2. 执行：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py run "{任务名}"
   ```
3. 捕获输出，完成后汇报结果摘要：
   ```
   ✅ 运行完毕: 「{任务名}」
   [stdout 摘要]
   ```
4. 若返回错误 "未找到任务"，列出当前可用任务：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py list
   ```

---

## LIST 状态

触发：见上表 **顺序 2**（整条消息仅为 `#rpa-list`，不区分大小写）。

含义：回答用户 **「当前有哪些已录制、可以使用的 RPA」** —— 与 `rpa_manager.py list` / `registry.json` 一致。

1. 回复："📋 正在列出当前可用的已录制 RPA 任务…"
2. 执行：
   ```bash
   python3 ~/.openclaw/workspace/skills/openclaw-rpa/rpa_manager.py list
   ```
3. 将 **stdout** 展示给用户（可适度排版）；末尾用一两句话说明：上面列出的就是 **现在能直接运行的任务名**；要跑其中某一个，发 **`#rpa-run:任务名`**（新对话）或 **`#运行:任务名`**（当前对话）。

---

## 生成代码质量（Recorder 模式自动保证）

由于录制时直接使用真实 CSS 选择器 + headed 浏览器验证，生成脚本天然满足：

1. **选择器真实**：所有 target 均来自 snapshot 返回的 DOM，不会猜选择器
2. **异常捕获**：每步用 `try/except`，失败时自动截图再 raise
3. **路径参数化**：输出路径通过 `CONFIG["output_dir"]` 配置
4. **可移植性**：生成的 `.py` 可脱离 OpenClaw 独立运行

---

## Recorder 指令日志（审计每一步 Playwright 对应代码）

- **录制过程中**：每执行一次 `record-step`，`rpa_manager` 向 `recorder_session/playwright_commands.jsonl` **追加一行 JSON**（JSONL）。
- **每行内容**：`command`（与发给录制器的 JSON 一致，含 `action` / `target` / `value` / `seq` 等）、`success`、`error`、`code_block`（该步写入最终 RPA 的 Python 片段）、`url`、`screenshot`。
- **会话边界**：首行为 `type: session, event: start`；`record-end` 成功前再追加 `event: end`，并把完整日志复制到 `rpa/{任务slug}_playwright_commands.jsonl`，便于与 `rpa/{任务slug}.py` 对照验收。
- **`record-end --abort`**：会删除整个 `recorder_session`，日志一并丢弃。

---

## 示例交互

```
用户：#自动化机器人
系统：🤖 OpenClaw RPA 实验室已就绪 ... 请发送：任务名称 + 空格 + 能力码

用户：每日资讯采集 A
系统：（deps-check A → record-start … --profile A）✅ Chrome 窗口已打开（含浏览器能力 A）...

用户：打开 example-news.com，搜索"AI"，把结果页前 5 条标题存到桌面 titles.txt
系统：
  （多步指令检测：3 个子任务，触发拆解）
  （执行 plan-set '["打开目标网站", "搜索关键词 AI", "提取前5条标题存文件"]'）
  （执行第 1 步：record-step goto）→ 截图
  📍 进度: 1/3 步已完成 ✅ 打开目标网站
  📸 截图: step_01_...png
  请回复「#继续」「1」或「next」执行第 2/3 步: 搜索关键词 AI

用户：1
系统：
  （plan-status → 第 2 步）
  （record-step snapshot → 在 📋 中找到搜索框选择器，如 input[name="q"]）
  （record-step fill input[name="q"] AI）
  （record-step press Enter）
  （plan-next）
  📍 进度: 2/3 步已完成 ✅ 搜索关键词 AI
  📸 截图: step_03_...png
  请回复「#继续」「1」或「next」执行第 3/3 步: 提取前5条标题

用户：next
系统：
  （plan-status → 第 3 步）
  （record-step scroll value=1200 → 滚动触发结果列表懒加载）
  （record-step wait value=1200）
  （record-step snapshot → 在 🗂️ 区块中找到含"results"的容器 [data-testid="results"]）
  （record-step extract_text [data-testid="results"] h3 a titles.txt limit=5）
  （plan-next → 全部完成）
  🎉 所有 3 步已全部完成！titles.txt 已写入桌面。
  可以说「#结束录制」生成 RPA 脚本。

用户：#结束录制
系统：✨ 生成成功！rpa/mei_ri_zi_xun_cai_ji.py（5 步，真实录制，选择器均经浏览器验证）

用户：#rpa-run:每日资讯采集
系统：▶️ 正在运行... ✅ 运行完毕。

用户：#运行:每日资讯采集
系统：▶️ 正在运行... ✅ 运行完毕。

用户：#rpa-list
系统：📋 正在列出…（输出 `rpa_manager.py list` 的注册任务列表）
```
---

## 其他资源

- 代码生成指导原则：[synthesis-prompt.md](synthesis-prompt.md)（区分 Recorder 直接拼装与 Legacy LLM 合成；二者均须对齐 `playwright-templates.md` / `recorder_server._build_final_script`，禁止用旧版 `get_by_role` + `networkidle` 极简骨架作为主路径）
- Playwright 代码模板库：[playwright-templates.md](playwright-templates.md)（骨架与原子步骤与 `recorder_server.py` 中 `_build_final_script` / `_do_action` 生成物一致：`CONFIG`、`_EXTRACT_JS`、`_wait_for_content`、`page.locator` + `page.evaluate`）
- RPA 管理工具命令一览：

  **计划管理（防超时）：**
  `rpa_manager.py plan-set '<json>'` | `plan-next` | `plan-status`

  **Recorder 模式（推荐）：**
  `rpa_manager.py record-start <task> [--profile A-N]` | `deps-check <A-N>` | `deps-install <A-N>` | `record-step '<json>'` | `record-status` | `record-end [--abort]`

  **通用：**
  `rpa_manager.py run <task>` | `list`（对话中也可发 **`#rpa-list`** 触发 LIST 状态）

  **Legacy：**
  `rpa_manager.py init <task>` | `add --proof <file> '<json>'` | `generate` | `status` | `reset`
