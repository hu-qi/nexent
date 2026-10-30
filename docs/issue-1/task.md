# Task Checklist: Issue #1

## Task 1: 需求文档 + 方案设计
- [x] Acceptance: docs/issue-1/{spec,plan,task}.md 就位，覆盖 Spec 六要素
- [x] Verify: 文件存在且内容与 Issue 验收标准一致
- [x] Files: docs/issue-1/*
- [x] Commit: `docs(issue-1): add spec/plan/task`

## Task 2: Python 包骨架 + 依赖声明
- [x] Acceptance: `src/nexent/__init__.py`、`pyproject.toml`、`requirements.txt`、`.gitignore` 就位
- [x] Verify: `python -c "import nexent"` 成功（pip install -e . 后）
- [x] Files: pyproject.toml, requirements.txt, .gitignore, src/nexent/__init__.py
- [x] Commit: `feat: #1 scaffold python package skeleton`

## Task 3: 检索模块 + 单元测试（TDD）
- [x] Acceptance: `src/nexent/resources/`（models/repository/memory）+ `tests/` 全绿
- [x] Verify: `pytest tests/ -v --junitxml=test-reports/junit.xml` 全绿；时间字段用范围断言
- [x] Files: src/nexent/resources/*.py, tests/test_*.py
- [x] Commit: `feat: #1 add tenant resource retrieval module skeleton with tests`

## Task 4: GitHub Actions CI
- [x] Acceptance: `.github/workflows/ci.yml` PR/push ci-check 触发；permissions contents: read（checks: write）；pip 缓存；junit artifact
- [x] Verify: YAML 语法解析通过 + 关键字段断言（触发/权限/缓存/artifact）
- [x] Files: .github/workflows/ci.yml
- [x] Commit: `ci: #1 add minimal github actions workflow`

## Task 5: README + 本地干跑脚本
- [x] Acceptance: README 含项目说明/快速开始/CI 徽章/secrets 清单；`scripts/local-ci.sh` 可复现 CI
- [x] Verify: 本地执行 `bash scripts/local-ci.sh` 全绿
- [x] Files: README.md, scripts/local-ci.sh
- [x] Commit: `docs: #1 add README and local CI dry-run script`

## 完成门（五轴自审查后）

- [x] ruff check 通过
- [x] pytest 全绿（含 junit.xml）
- [x] 凭据 grep 扫描零明文
- [x] git push feat/issue-1 成功
