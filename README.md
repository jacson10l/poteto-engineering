# Poteto 工程闭环 · Agent Skill

让正确实现成为 Agent 最容易走通的路径。

A practical, evidence-driven engineering skill inspired by the principles shared by Lauren Tan (@poteto). Chinese instructions, reusable verification templates, and a dependency-free Python evidence-manifest validator.

## 它解决什么问题

当工程环境缺乏约束和验证能力时，更多 Agent 和 Token 只会放大返工。这份 Skill 把五项原则落实为操作流程：改善历史代码示例，把重复纠错变成机器约束，提供可运行工具，用真实证据交付，并按风险增加测试或形式化验证。

| 模式 | 适用任务 | 结果 |
| --- | --- | --- |
| `audit` | 体检工程、评估 Agent 交付能力 | 有证据的缺口与优先事项；只读分析 |
| `harden` | 建立类型、Lint、架构规则和验证入口 | 实际可执行、能抓住坏例子的工程约束 |
| `deliver` | 开发、修复、重构 | 改动、真实验证、证据和适量防复发机制 |

核心流程：**定义验收 → 建立基线/复现 → 实施改动 → 真实验证 → 交付证据 → 防止复发**。

## 获取与使用

```bash
git clone https://github.com/jacson10l/poteto-engineering.git
```

技能的完整目录是 [`skills/poteto-engineering`](skills/poteto-engineering)。将整个目录导入支持 `SKILL.md` 的 Agent 技能系统，保留 `references/`、`assets/`、`scripts/` 和 `agents/` 的相对位置。具体导入入口和调用语法由所用 Agent 决定。

也可以让有文件读取能力的 Agent 读取 [`SKILL.md`](skills/poteto-engineering/SKILL.md)，然后按其中流程执行任务。

示例请求：

```text
使用 poteto-engineering 体检当前项目，找出阻碍 Agent 可靠交付的三个主要问题。
```

```text
使用 poteto-engineering 修复这个问题，实际运行验证，并把重复犯错的原因转成机器约束。
```

## 内容导航

| 文件 | 作用 |
| --- | --- |
| [SKILL.md](skills/poteto-engineering/SKILL.md) | 统一入口、工作流与完成条件 |
| [environment.md](skills/poteto-engineering/references/environment.md) | 环境体检、改造优先级与历史代码治理 |
| [guardrails.md](skills/poteto-engineering/references/guardrails.md) | 纠错转规则；Vue/TS、Electron/Tauri 等适配示例 |
| [verification.md](skills/poteto-engineering/references/verification.md) | 实测、UI 证据、性能与形式化验证边界 |
| [delivery.md](skills/poteto-engineering/references/delivery.md) | 交付状态、受控自动化与质量指标口径 |
| [provenance.md](skills/poteto-engineering/references/provenance.md) | 来源、原创适配与数字核验状态 |
| [验证契约模板](skills/poteto-engineering/assets/verification-contract.template.md) | 固定启动、操作、断言、取证和清理入口 |
| [证据清单模板](skills/poteto-engineering/assets/evidence.template.json) | 将验收条件关联到检查与证据文件 |
| [validate_evidence.py](skills/poteto-engineering/scripts/validate_evidence.py) | 校验清单、引用、版本标签及文件 SHA-256 |

## 运行校验器与测试

需要 Python 3.9+，仅使用标准库。模板默认标记为未执行，因此直接验证空模板会失败；实际运行检查并填写证据后再验证。

```bash
python3 skills/poteto-engineering/scripts/validate_evidence.py /path/to/evidence/manifest.json
python3 -m unittest discover -s skills/poteto-engineering/scripts -p 'test_*.py' -v
```

校验器的 `manifest-consistent` 只表示记录和文件一致，不能认证测试是否真实执行、截图内容是否正确，也不代表允许合并。Agent 仍须运行产品、检查输出并查看视觉证据。

## 范围与来源

这是独立整理的工程适配版，不是 Poteto 官方 pstack 的原样分发，也不隶属于或获得其背书。方法方向参考 [pstack](https://github.com/cursor/plugins/tree/main/pstack) 的公开材料；具体来源和核验状态见 [provenance.md](skills/poteto-engineering/references/provenance.md)。

不承诺固定 PR 产量或回滚率。形式化检查必须交代性质、假设、边界和代码对应关系；自动合并沿用项目已有授权与质量门槛。
