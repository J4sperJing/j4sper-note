---
title: 0-入门概念
description: agent的入门概念
date: 2026-09-15
tags:
  - books
  - ai-agent-book
order: 0
---
# Agent组成
一个最小极简的agent，需要：
**Agent = LLM + 上下文 + 工具**

对于生产可用的，harness工程所做的：
**Agent = Model + Harness**
**Harness = 上下文管理 + 工具接口 + 约束 + 验证 + 纠正**

加入了 约束、验证、纠正，来约束agent 能做的范围、 结果是否正确、错误时如何补救

一个agent极简伪代码骨架：

```python
observation = Environment.observe()
trajectory = [observation]
while true:
	actions = Model(Harness.build_context(trajectory))
	if len(actions) == 0:
		break
	allowed_actions = Harness.constrain(actions)
	observation = Environment.apply(allowed_actions)
	if not Harness.verify(Environment):
		observation = Harness.correct(Environment)
	trajectory.append(allowed_actions, observation)
```

# Agent的跃近史
1、Prompt Engineering：优化输入的提示词
2、Context Engineering：系统指令、工具定义、对话历史、外部知识
3、Harness：上下文与工具接口、约束机制、验证手段、反馈循环和错误恢复。加入了更多的工程限制内容，更生产级
4、Loop Engineering：从单次执行，到跨轮次执行
5、Graph Engineering：

# Agent系统构建的三个原则：
## 1、**保持简单**
从最简单的方案开始，只在确实必要时才增加复杂度。直接的 API 调用优于复杂的框架，清晰的代码优于聪明的抽象。因为每多一层抽象都会成为以后调试时新的盲区。
# 2、**保持透明**
明确显示 Agent 的规划步骤、执行日志和决策轨迹——这不只是为了调试方便，也是让用户建立信任的前提。因为黑箱里的错误一旦发生，外部观察者既无法定位也无法纠正。做好trace！
# 3、**设计好工具接口**
**工具接口（ACI，Agent-Computer Interface）**。ACI 强调的是从 Agent 视角设计接口（让 Agent 容易理解和使用），而非传统 API 从程序员视角设计接口。工具的命名和参数要直观，容易误用的地方要从设计上让错误无法发生——比如 SIM 卡的缺角让卡片只能从一个方向插进卡槽，避免了用户插反的错误；微波炉门没关好就绝不加热，避免了用户开门加热的危险行为。这种“用设计消除错误”的思路，在制造业里有一个专门的术语，叫**防呆**（Poka-yoke），源自丰田生产体系。设计不好的工具会让再强的模型也频繁出错——因为模型与工具之间唯一的沟通通道就是接口本身，模糊的接口会被模型放大成系统性的错误。

# Agent技术

## Model
### 1. 如何进行模型选型？
>先大致说下模型种类：
>普通对话模型、reasoning、grounding、生图（视频）模型、VLM等

简单来说，首先需要考虑开源、闭源模型两类。从成本、能力、数据合规角度来选。
然后，首先考虑的是模型能力，不只是排行榜，也要做好评测，是否适用于自己的任务，尤其是工具调用能力。
其次是模型的策略边界，比如模型可能支持，但实际上不允许用户调用，比如网络安全、模型蒸馏、模型提取、隐私数据和高风险操作等。比如Grok和其他模型，边界肯定不同。
接下来，大部分agent需要选择支持reasoning的模型，一般来说表现会好一些，因为需要多步思考或者动态决策。除非是computer use这种，只需要识别、给出位置这样的**Grounding**之类的。
性能上，需要看输出token速度
最后，如果需要多模态能力，就需要有多模态能力的模型。

详细可见的能力评测方式可见：[]()

## Harness
### 1、编排模式
在构建 LLM 应用时，应遵循“从简单到复杂”的原则：首先考虑单个 LLM 调用。如果通过优化提示词和上下文示例就能解决问题，就不要引入 Agent 系统。当需要多步骤处理时，对于可以清晰分解为固定子任务的场景，考虑使用工作流。只有当需要动态决策和灵活的执行路径时，才使用自主 Agent。需要记住的是：Agent 系统通常会用延迟和成本换取更好的任务性能，应该谨慎权衡这种交换是否值得。

***怎么做？***
先给一个能力足够的 Agent 清晰的目标、必要的上下文和可组合的工具，用自然语言告诉它如何像人一样查证、比较、处理冲突；程序只固化权限、不得覆盖原始材料、原子发布等必须始终成立的边界。只有业务约束本身要求，或评估反复暴露出某类稳定失败时，才把对应步骤升级为专门的验证器、独立 Agent 或确定性流程。好的结构不是替 Agent 预演全部思考，而是守住边界，并把边界内的决策空间还给模型。

