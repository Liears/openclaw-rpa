# openclaw-rpa

**[English](README.md)** | 中文

借助 **AI**，把你在**常见网站**上的操作，以及需要的**本机文件**行为，录制成可重复运行的 **RPA 脚本**（Python / Playwright）。日常执行**直接跑脚本**，不必每次让模型现场点网页——**省算力**，且步骤按录制固定执行，**更稳、少受模型幻觉影响**。

**涵盖：** 浏览器里的真实交互；脚本中也可包含读写、整理本机文件等（可与网页分开或组合）。

**举例：** 定时跑同一段下单/填表脚本；或在脚本里加几行只整理下载目录——重复执行时都不再走一遍「模型当场操作」。

## 环境要求

- **Python 3.8+**（建议 3.10+）
- **pip** 以及用于 `pip install` 与 Playwright 浏览器下载的网络

## 安装（推荐）

在本仓库根目录执行：

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

将创建 **`.venv`**，按 `requirements.txt` 安装 Python 依赖，并执行 **`playwright install chromium`**。

之后每次使用本技能前先激活虚拟环境：

```bash
source .venv/bin/activate
```

### 手动安装

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
python -m playwright install chromium
```

### 环境自检

```bash
python3 envcheck.py
# 或
python3 rpa_manager.py env-check
```

`record-start` 与 `run` 也会检查 Python + Playwright，并在可能时**自动安装 Chromium**（与原先行为一致）。

## 首次配置（对话语言）

仓库中仅包含 **`config.example.json`**（默认 **`en-US`**）。

```bash
python3 scripts/bootstrap_config.py
```

会从示例生成 **`config.json`**。可编辑 `"locale"`，或使用：

```bash
python3 scripts/set_locale.py zh-CN
python3 scripts/set_locale.py en-US
```

详见 **`LOCALE.md`**。修改语言后请开启新的 OpenClaw 会话，或让智能体重新读取 **`SKILL.md`** / **`SKILL.*.md`**。

## 快速开始（命令行）

```bash
python3 rpa_manager.py env-check
python3 rpa_manager.py list
python3 rpa_manager.py run wikipedia
```

录制流程：`record-start` → `record-step` → `record-end`（详见 `rpa_manager.py` 文件内说明）。

## 示例脚本

预生成脚本与指令日志在 **`rpa/`** 下。建议入门：

| 脚本 | 说明 |
|------|------|
| `rpa/wikipedia.py` | 稳定公网站点（英文） |
| `rpa/wiki.py` | 同类流程，不同命名 |
| `rpa/豆瓣电影.py` | 中文界面示例（请遵守站点规则） |
| `rpa/电商网站购物v10.py` | 电商类流程示例（仅供演示） |

**examples/README.md** 中有更完整的推荐与注意事项。

## 许可证

[Apache License 2.0](LICENSE) — 版权 © 2026 openclaw-rpa contributors。
