# OpenClaw-RPA

**AI Agent 的"RPA 编译器"** — 一次录制，永久回放为确定性 Python 脚本。

## 仓库结构

```
openclaw-rpa/
├── README.md              # 本文件
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
    ├── registry.json      # 任务注册表
    └── requirements.txt   # Python 依赖
```

## 安装

```bash
# 安装依赖
pip install -r rpa/requirements.txt

# 安装浏览器
playwright install chromium
```

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
