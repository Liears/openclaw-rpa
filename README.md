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

### 安装到其他 agent

如果目标 agent 的 skill 机制是“一个 skill 对应一个文件夹，文件夹内包含 `SKILL.md`”，那么安装方式很直接：

1. 把本仓库里的 `rpa/` 整个文件夹复制到目标 agent 的 skills 目录。
2. 进入复制后的 `rpa/` 目录。
3. 执行：

```bash
./scripts/install.sh
```

4. 验证：

```bash
python3 scripts/rpa_manager.py help
```

说明：

- 不要只复制 `SKILL.md`，要复制整个 `rpa/` 文件夹。
- 运行依赖在 `scripts/`、`requirements.txt`、`registry.json` 中。
- 录制生成的脚本默认写到 skill 包内部的 `rpa/rpa/` 目录。
- 登录 Cookie 保存在用户目录 `~/.openclaw/rpa/sessions/`，不在 skill 包内。

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
