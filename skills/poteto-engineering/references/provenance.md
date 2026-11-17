# 来源与适配边界

核对日期：2026-11-17。

本 Skill 综合用户提供的实践总结和 Lauren Tan 的公开材料。执行模式、验收要求、风险分层、模板和 Python 校验器是独立整理的适配方案。

- [AI Engineer 官方演讲《All Code Is Slop (Except Mine)》](https://ai.engineer/code/2026/talks/lauren-tan) 含演讲录像、时间点和机器转录。转录可能错写产品名称。
- [AI Engineer 演讲者资料](https://ai.engineer/speakers/lauren-tan) 确认 Lauren Tan 在 SpaceXSI 的 **Grok Bot** 团队工作。
- [pstack 项目说明](https://github.com/cursor/plugins/blob/main/pstack/README.md)、[验证与交付指南](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md) 和 [形式化验证维护指引](https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-formal-verification-skill/SKILL.md) 提供工作流与验证的公开背景。

## 演讲中的数据口径

Lauren Tan 在 2026 年 11 月的演讲中报告，团队上月约有 **11,000 个 PR 交付生产**，近期 PR 回退比例约 **0.5%**，客户端约每日发布一个稳定版。她说约 **227 人**在 10 月贡献了至少一个 PR。演讲未将这 227 人全部归为团队外部贡献者。她也报告启动、打字与聊天切换等性能较上线时改善。

这些是演讲者报告的团队结果。演讲未给出完整回退分母、观察窗口或独立审计。约六个月是 Lauren Tan 描述自己的实践时间。她提到的 **70% Token** 来自另一位工程师的个人分享，适合作为验证投入案例。保留这些数字用于理解案例，项目验收采用自己的质量、成本和交付基线。
