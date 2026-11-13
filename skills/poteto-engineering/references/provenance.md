# 来源与适配边界

核对日期：2026-11-13。

## 本 skill 的依据

用户直接提供五项原则：改善历史代码示例；减少依赖 AGENTS.md 的人工提醒，把纠错变成机器约束；提供运行/检查工具；用真实证据交付修复；增加自动测试和形式化验证投入。

本 skill 的模式划分、验收清单、风险分级、技术栈示例、指标口径和 Python 校验器是针对这些原则原创整理的工程实施方案，不是 Lauren Tan / @poteto 的原话或官方发布。

## 查阅的一手材料

- [pstack 官方项目说明](https://github.com/cursor/plugins/blob/main/pstack/README.md)：有统一入口及按任务选择其他工作流的设计。
- [pstack 验证与交付指南](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md)：强调明确完成条件、实际运行产品，以及建立可复用的验证能力；形式化检查应说明范围和限制。
- [pstack 形式化验证维护指引](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-formal-verification-skill/SKILL.md)：提醒代码改变后核对模型，区分模型漂移和产品缺陷。

以上仅用于核对方法方向，未复制其 skill 正文、脚本或模型配置。不要求用户安装 pstack，不冒用其官方身份。

## 数字不作为已审计事实

用户提到团队月交付 11,000 PR、回滚率 0.5%、环境打磨六个月。检索找到了作者发布 11,000 PR 演讲预告的镜像线索，但本次未能直接读取原帖，也未取得完整原始演讲、统计明细或审计资料。

因此这些数字仅作为用户提供的背景，不用于承诺产能、建立质量门槛或断言因果。本 skill 不把团队月度总量、个人月度量和其他月份数字混为一谈。

原帖定位线索：[演讲预告](https://x.com/poteto/status/2119841446308221152)。需要对外引用具体数字时，另行核对原演讲、时间窗口、团队规模和回滚分母。
