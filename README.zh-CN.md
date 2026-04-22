# OpenClaw-RPA

**AI Agent 的"RPA 编译器"** — 一次录制，永久回放为确定性 Python 脚本。

## 仓库结构

```
openclaw-rpa/
├── README.zh-CN.md        # 本文件
├── .gitignore
└── rpa/                   # ⭐ Skill 包（可独立分发）
    ├── SKILL.md           # 核心协议与触发词
    ├── scripts/           # 运行脚本
    │   ├── rpa_manager.py
    │   ├── recorder_server.py
    │   └── envcheck.py
    ├── references/        # 代码模板与合成原则
    │   ├── playwright-templates.md
    │   └── synthesis-prompt.md
    ├── examples/          # 示例脚本（可直接运行）
    │   ├── amazonbestseller.py
    │   ├── airbnb民宿比价分析v11.py
    │   └── ...
    ├── pkgs/              # 离线安装包
    │   ├── *.whl          # Python 依赖（15 个包）
    │   └── browsers/      # Chromium 浏览器二进制
    ├── registry.json      # 任务注册表
    └── requirements.txt   # Python 依赖
```

## 在线安装

```bash
# 安装 Python 依赖
pip install -r rpa/requirements.txt

# 安装浏览器
playwright install chromium
```

## 离线安装（完全断网环境）

```bash
# 1. 安装 Python 依赖
pip3 install --no-index \
  --find-links=rpa/pkgs/ \
  --break-system-packages \
  playwright httpx openpyxl python-docx

# 2. 安装浏览器（二进制）
PLAYWRIGHT_BROWSERS_PATH=0 \
  python3 -m playwright install --with-deps chromium
```

**离线包大小：**
- Python whl：`rpa/pkgs/` 约 51MB
- 浏览器二进制：`rpa/pkgs/browsers/` 约 280MB
- **合计约 330MB**

> 首次安装成功后，后续运行 `rpa/scripts/rpa_manager.py` 无需任何网络连接。

## 快速开始

```bash
# 查看可用任务
python3 rpa/scripts/rpa_manager.py list

# 运行任务
python3 rpa/scripts/rpa_manager.py run "任务名"
```

## 作为 Skill 使用

将 `rpa/` 目录复制到你的 OpenClaw agent 的 `skills/` 目录即可。

GitHub: https://github.com/laziobird/openclaw-rpa
