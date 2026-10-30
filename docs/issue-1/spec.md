# Spec: Issue #1 — 租户资源管理检索（GitHub Actions 驱动）

> 承接 ModelEngine-Group/nexent 方向（原引 ModelEngine/nexent 已 404，实际公开仓为 ModelEngine-Group/nexent）。
> Issue Agent 已在 Issue #1 发布 Spec，本文件为 coding 侧落仓确认版（保持验收标准一致）。

## Objective

在空仓 `hu-qi/nexent` 上完成仓库初始化并落地最小可跑的 GitHub Actions CI：

1. 仓库骨架：Python 项目结构（`src/` + `tests/` + 依赖声明）+ `README.md`
2. 检索模块骨架：`src/nexent/resources/` 租户资源管理检索的基础目录结构与入口文件（对标上游 `sdk/nexent/` 的包布局风格：扁平包 + `__init__.py` + 领域子包）
3. `.github/workflows/ci.yml`：PR / push → main 触发 checkout → 依赖安装 → lint → 单测
4. 测试报告 artifact：pytest 输出 junit-xml，`upload-artifact` 上传

## Upstream Baseline（上游基线核查结论）

| 项 | 结论 |
|---|---|
| 上游仓库 | `ModelEngine-Group/nexent`（公开，6k+ stars）；原引 `ModelEngine/nexent` 404 |
| 上游 #6 | "✨ add embedding config in frontend"（已关闭）——方向性参考，非直接需求 |
| 上游包布局 | `sdk/nexent/`：扁平 Python 包（`core/`、`memory/`、`storage/`、`vector_database/` 等领域子包），`pyproject.toml`，Python 3.11 |
| 上游 CI 风格 | `permissions: contents: read`、concurrency 取消旧跑、路径过滤、junit/coverage 产出 |
| 本仓决策 | 空仓从零搭建骨架，**不复制上游代码**（保持零依赖体积），仅对齐结构风格与 CI 安全约定 |

## Tech Stack

- Python >= 3.11（本仓声明 `>=3.11`；CI 用 `actions/setup-python` 官方 runner Python）
- 测试：pytest + junit-xml
- Lint：ruff（check，不 auto-fix，保证 CI 可判定）
- 依赖声明：`pyproject.toml`（PEP 621）+ `requirements.txt`（CI 安装入口）

## Commands

```
安装:      pip install -r requirements.txt
Lint:      ruff check .
测试:      pytest tests/ -v --junitxml=test-reports/junit.xml
本地干跑CI: bash scripts/local-ci.sh
```

## Project Structure

```
.github/workflows/ci.yml    → CI 流水线（PR/push main）
docs/issue-1/               → 本 Issue 文档（spec/plan/task）
scripts/local-ci.sh         → 本地一键复现 CI 步骤（lint + test + junit 报告）
src/nexent/                 → 检索模块包
  __init__.py               → 包入口 + 版本
  resources/                → 租户资源管理检索模块（本期骨架）
    __init__.py             → 模块入口（公共 API re-export）
    models.py               → 资源数据模型（TenantResource 等纯数据类）
    repository.py           → ResourceRepository 接口（索引/查询/删除契约）
    memory.py               → 内存实现（骨架期默认实现，可测试）
tests/                      → 单元测试（镜像 src 结构）
tests/test_models.py / test_repository.py / test_memory.py
pyproject.toml / requirements.txt / .gitignore / README.md
```

## Code Style

- 类型注解必写（骨架期即建立约束）；docstring 简洁中文+英文签名
- 纯数据模型用 `dataclass`；接口用 `abc.ABC`（对标上游 `VectorDatabaseCore` 风格）
- 示例：

```python
@dataclass
class TenantResource:
    tenant_id: str
    resource_id: str
    resource_type: str
    content: str
    created_at: datetime
```

## Testing Strategy

- 框架：pytest；报告：junit-xml（CI artifact）
- 纯逻辑单测（无 I/O、无网络）：模型构造/校验、仓储接口契约、内存实现行为
- 时间断言规范（SKILL.md 六）：**禁止毫秒级相等比较**——`created_at` 用范围断言或固定时钟注入

## Boundaries

- Always: 提交前跑 lint + pytest；时间字段范围断言
- Ask first: 变更 CI 触发条件；引入新的重量级依赖
- Never: 提交任何明文凭据（AK/SK/token）；绕过 PR 直推基线

## Secrets 规范（凭据管理）

- 代码/CI 中仅通过 `${{ secrets.* }}` 引用（如后续华为云集成用 `HUAWEICLOUD_AK`/`HUAWEICLOUD_SK`），仓库内零明文
- README 列出需配置的 secrets 清单；本期 CI 不消费任何 secret（最小权限：`contents: read`）

## Success Criteria（与 Issue 验收一致）

1. 仓库初始化完成（骨架 + README）
2. `.github/workflows/ci.yml` 就绪，PR / push main 触发，步骤全绿
3. pip 依赖缓存生效（setup-python `cache: 'pip'`）
4. 仓库无明文 AK/SK/token（grep 扫描通过）
5. Workflow 默认权限 `contents: read`（按需 `checks: write`）
6. CI 产出测试报告 artifact（junit-xml）可下载
