# RPA Skill

这个仓库已经从原始项目仓库重构为一个可分发的 skill 包仓库。

## 仓库结构

- `rpa/`
  真正的 skill 包目录，可直接复制到其他 agent 的 skills 目录中使用。
- `README.md`
  面向人阅读的说明文件。
- `LICENSE.md`
  仓库许可证。

## skill 包里有什么

`rpa/` 目录包含：

- `SKILL.md`
  给 agent 读取的核心协议
- `agents/openai.yaml`
  skill 的展示元数据
- `scripts/`
  运行时脚本，包括录制、回放、依赖检查与安装
- `requirements.txt`
  Python 依赖
- `registry.json`
  任务注册表，默认是空的
- `rpa/`
  录制后生成的脚本输出目录

## 这个 skill 能做什么

这个 skill 用来把浏览器、API、Excel、Word 操作录制成可回放的 Python Playwright 脚本，适合：

- 录制新的 RPA 自动化流程
- 回放已录制任务
- 保存并复用登录 Cookie
- 执行浏览器 + 文件 + API 的混合自动化

## 安装到其他 agent

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

## 本地使用

进入 skill 目录：

```bash
cd rpa
```

安装依赖：

```bash
./scripts/install.sh
```

查看帮助：

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
