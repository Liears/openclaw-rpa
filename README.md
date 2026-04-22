# RPA Skill

这个仓库现在按“外层说明 + 内层 skill 包”组织。

## 目录结构

- `rpa/`
  真正的 skill 包目录，包含：
  - `SKILL.md`：给 agent 读取的核心协议
  - `agents/openai.yaml`：skill UI 元数据
  - `scripts/`：运行时脚本
  - `requirements.txt`：Python 依赖
  - `registry.json`：任务注册表
  - `rpa/`：录制生成脚本的输出目录

- `README.md`
  面向人的说明文件，介绍 skill 的用途和使用方法。

## skill 能做什么

这个 skill 用来把浏览器、API、Excel、Word 操作录制成可回放的 Python Playwright 脚本，适合：

- 录制新的 RPA 自动化流程
- 回放已录制任务
- 保存并复用登录 Cookie
- 执行浏览器 + 文件 + API 的混合自动化

## 使用方式

如果你是把它当作 skill 包使用，核心内容在：

- [rpa/SKILL.md](rpa/SKILL.md)

如果你要在本地运行它：

1. 进入 skill 目录：

```bash
cd rpa
```

2. 安装依赖：

```bash
./scripts/install.sh
```

3. 查看帮助：

```bash
python3 scripts/rpa_manager.py help
```

## 常用命令

```bash
python3 scripts/rpa_manager.py list
python3 scripts/rpa_manager.py run "任务名"
python3 scripts/rpa_manager.py record-start "任务名" --profile A
python3 scripts/rpa_manager.py record-end
python3 scripts/rpa_manager.py login-start https://example.com/login
python3 scripts/rpa_manager.py login-done
```

## 说明

- 根目录 README 面向人阅读
- `rpa/` 目录面向 skill/agent 运行
- 录制后生成的脚本默认写到 `rpa/rpa/`
