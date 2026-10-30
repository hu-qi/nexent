# Implementation Plan: Issue #1 — 仓库初始化 + 最小 CI

## Overview

空仓从零搭建 Python 项目骨架（src 布局 + 检索模块）并落地 GitHub Actions 最小 CI（lint + 单测 + junit artifact + pip 缓存 + 权限收敛）。上游 `ModelEngine-Group/nexent` 已核查为公开仓，但其 `sdk/` 体量巨大且依赖重；按 Spec 决策不复制上游代码，仅对齐包布局风格与 CI 安全约定。

## Architecture Decisions

| 决策 | 选择 | 理由 |
|---|---|---|
| 包布局 | `src/nexent/` src-layout | 对标上游 `sdk/nexent/` 扁平包风格；src-layout 防误 import，CI 里 `pip install -e .` 或 PYTHONPATH 均可 |
| 检索模块命名 | `src/nexent/resources/` | "租户资源管理检索" 直译领域包，后续可扩展 `vector_database/` 等兄弟包 |
| Lint 工具 | ruff（仅 check） | 零配置、快、CI 可判定；不引入 auto-fix 步骤保证步骤可审计 |
| 测试报告 | pytest junit-xml + upload-artifact | Issue 验收标准明确要求 junit-xml + artifact |
| Python 版本矩阵 | 3.11 单版本起步 | 上游要求 3.11；本地环境为 3.14（兼容写法，`requires-python >=3.11`） |
| 原子提交 | 5 个（见 task.md） | 文档 → 骨架 → 测试 → CI → README+gitignore，每个提交独立可回滚 |

## Task List

### Phase 1: 文档与地基
- [x] Task 1: spec/plan/task 文档（docs/issue-1/）

### Phase 2: 代码骨架（TDD）
- [x] Task 2: Python 包骨架 + 依赖声明（pyproject.toml/requirements.txt/.gitignore）
- [x] Task 3: 检索模块（models/repository/memory + 入口导出）+ 单元测试

### Phase 3: CI 与文档
- [x] Task 4: .github/workflows/ci.yml（权限收敛 + pip 缓存 + junit artifact）
- [x] Task 5: README.md（说明 + 快速开始 + secrets 清单 + CI 徽章）+ 本地干跑脚本

## Checkpoint: 完成门

- [x] 本地 ruff check 通过
- [x] 本地 pytest 全绿 + junit.xml 产出
- [x] 明文凭据 grep 扫描零命中
- [x] `act`/语法级校验 workflow YAML（无 runner 池则静态校验）

## Risks and Mitigations

| 风险 | 影响 | 缓解 |
|---|---|---|
| 空仓首次推送后 PR base=ci-check 不存在 | 高 | 首推 `feat/issue-1`；若平台不允许空 base PR，则由 QA/人工先合入 ci-check（PR 依然创建） |
| 本地 Python 3.14 与 CI 3.11 差异 | 低 | 只用稳定标准库语法；`requires-python >=3.11` |
| HTTP2 帧错误导致 push 失败 | 中 | 已预置 `http.version HTTP/1.1`；重试 ≤3 次 |
| CI 全绿需真实 runner 验证 | 中 | 合并后由 push ci-check 自动触发验证；PR 阶段以语法/结构校验为准 |

## Open Questions

无（Spec 已由 Issue Agent 发布并确认 ready）。
