# nexent

> 租户资源管理检索（tenant resource management & retrieval）— 承接 [ModelEngine-Group/nexent](https://github.com/ModelEngine-Group/nexent) 方向的独立实现仓。

[![CI](https://github.com/hu-qi/nexent/actions/workflows/ci.yml/badge.svg)](https://github.com/hu-qi/nexent/actions/workflows/ci.yml)

## 项目简介

本仓库为「租户资源管理检索」能力的代码基座：

- **多租户隔离**：资源按 `tenant_id` 严格隔离（仓储层强约束）
- **检索骨架**：`ResourceRepository` 存储契约 + 内存参考实现，后续替换为 Elasticsearch/Milvus 等持久化后端
- **CI 门禁**：GitHub Actions 自动化 lint + 单测 + 测试报告 artifact

当前为**骨架阶段**（Issue #1 首期交付）：目录结构 + 模块入口 + 最小 CI，功能迭代在后续 Issue 中展开。

## 快速开始

```bash
# 安装（骨架期零运行时依赖）
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 安装开发/测试工具链
pip install -r requirements-dev.txt

# 本地一键复现 CI（lint + test + junit 报告）
bash scripts/local-ci.sh
```

### 使用示例

```python
from datetime import datetime, timezone

from nexent.resources import InMemoryResourceRepository, TenantResource

repo = InMemoryResourceRepository()
stored = repo.add(
    TenantResource(
        tenant_id="tenant-a",
        resource_id="",  # 留空则自动生成
        resource_type="document",
        content="2026 Q1 租户资源报告",
        created_at=datetime.now(timezone.utc),
    )
)
print(repo.search("tenant-a", "报告"))  # -> [TenantResource(...)]
```

## 目录结构

```
.github/workflows/ci.yml   # CI：PR/push main → lint → 单测 → junit artifact
src/nexent/
  resources/               # 租户资源管理检索模块（本期骨架）
    models.py              # TenantResource 数据模型
    repository.py          # ResourceRepository 存储契约（ABC）
    memory.py              # 内存参考实现（可测试）
tests/                     # pytest 单元测试（23 个用例）
scripts/local-ci.sh        # 本地 CI 干跑脚本
docs/issue-1/              # Issue #1 需求/方案/任务文档
pyproject.toml             # PEP 621 包元数据 + ruff/pytest 配置
requirements.txt           # 运行时依赖（骨架期为空）
requirements-dev.txt       # 开发/测试工具链
```

## CI

`.github/workflows/ci.yml` 在 **PR / push → main** 时触发：

| 步骤 | 说明 |
|---|---|
| checkout | `actions/checkout@v4` |
| 依赖安装 | `actions/setup-python@v5`（Python 3.11）+ 内置 **pip 缓存** |
| lint | `ruff check .` |
| 单测 | `pytest --junitxml=test-reports/junit.xml` |
| artifact | `actions/upload-artifact@v4` 上传 junit 测试报告（保留 14 天） |

**权限收敛**：默认 `contents: read`，按需 `checks: write`，无其他写权限。

## Secrets 配置清单

仓库内**零明文凭据**。后续华为云/ModelArts 集成（双轨）需在 GitHub 仓库
`Settings → Secrets and variables → Actions` 配置：

| Secret | 用途 | 当前状态 |
|---|---|---|
| `HUAWEICLOUD_AK` | 华为云访问密钥 AK | 预留（集成 job 注释在 ci.yml 中） |
| `HUAWEICLOUD_SK` | 华为云访问密钥 SK | 预留（同上） |

代码与 workflow 中仅通过 `${{ secrets.* }}` 引用；`.gitignore` 已排除 `.env`/`*.pem`/`*.key`/`secrets/`。

## 开发约定

- Python `>=3.11`；src-layout；类型注解必写
- 测试断言：时间字段使用**范围断言**（禁止毫秒级相等比较）
- 提交前本地过门禁：`bash scripts/local-ci.sh`

## License

Apache-2.0（与上游 nexent 一致）。
