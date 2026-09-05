# Sergey Levine：近期研究趋势分析

> 更新时间：2026-09-05  
> Google Scholar：[Sergey Levine](https://scholar.google.com/citations?hl=en&user=8R35rCwAAAAJ&view_op=list_works&sortby=pubdate)

> 保存说明：本文件保留研究者分析的长版讨论内容，而不是仅保留结论摘要。由于旧回复的逐字文本已无法从历史检索中恢复，以下 Levine 部分是依据当时保留下来的论文、论点和比较框架所作的完整重建版，不冒充逐字聊天记录。

## 原始讨论问题

用户首先询问了 test-time training 与 in-context learning 的含义、二者在机器人和 AI 中的趋势，以及它们如何与 VLA、RL 和 world model 相连。随后提供 Sergey Levine 的 Google Scholar 页面，希望分析其近期论文并判断机器人和 AI 的当前趋势。

## 0. 讨论所使用的概念背景

### 0.1 In-context learning 是什么？

In-context learning（ICL）是指模型在推理时根据输入上下文中的示例、指令、历史经验或反馈改变输出行为，但通常**不更新模型参数**。对语言模型而言，context 可以是 few-shot demonstrations；对机器人而言，它可以是：

- 一段人类或机器人示范；
- 当前环境的短视频；
- 先前任务的成功与失败记录；
- 自然语言形式的经验总结；
- 当前任务的子目标、偏好或约束；
- 长期记忆中检索出的相关技能。

因此，机器人 ICL 不应只理解成“在 prompt 中放几个例子”，更准确地说，它是在一次部署过程中，通过上下文重新解释任务、选择策略或组合已有技能。

### 0.2 Test-time training 是什么？

Test-time training（TTT）通常指模型在测试或部署过程中，利用当前无标签/弱标签观测、自监督损失、任务反馈或在线交互，**对参数或内部状态进行更新**。它与 ICL 的基本区别是：

| 方法 | 是否更新参数 | 主要适应载体 |
|---|---:|---|
| In-context learning | 通常不更新 | prompt、示范、记忆、隐状态 |
| Test-time training | 通常更新部分参数或状态 | 自监督损失、在线经验、任务反馈 |
| Online RL fine-tuning | 更新 | reward、success/failure、value estimate |
| Test-time search | 不一定更新 | 采样、规划、value/verifier 筛选 |

机器人文献中这些术语边界并不完全统一。很多论文虽然不称自己为 TTT，却在做 deployment-time adaptation；另一些所谓 test-time learning 实际上是 search、memory retrieval 或 policy steering，而不是梯度更新。

### 0.3 为什么它们在机器人中重新受到重视？

机器人部署天然存在 distribution shift：家庭、物体、用户、相机、动力学与训练数据不同。仅靠一个冻结的 foundation policy 很难覆盖所有组合。因此当前趋势不是在 ICL、TTT 和 RL 中三选一，而是组合它们：

\[
\text{pretrained prior}
+ \text{context adaptation}
+ \text{test-time search}
+ \text{selective parameter update}
+ \text{real-world feedback}.
\]

Levine 的近期工作可以被视为这一组合在通用机器人策略上的系统化实现。

## 一句话结论

Sergey Levine 当前的核心方向，是把机器人学习从“针对单项任务训练一个策略”推进为一个可规模化的通用机器人学习系统：先用异构机器人数据、语言和视觉知识训练 VLA/generalist policy，再通过记忆、价值函数、强化学习和部署经验持续提高可靠性。

可以把他的核心问题概括为：

> 如何构建一个能力足够广、能够组合技能，并且可以在部署后继续改进的通用机器人策略？

## 1. 当前主要趋势

### 1.1 VLA 正在成为机器人策略的基础接口

Levine 近期与 Physical Intelligence 团队的工作表明，VLA 不再只是“视觉和语言模型后接一个动作头”，而逐渐成为连接多机器人数据、自然语言指令、语义推理和连续控制的统一策略。

- [π0.5](https://arxiv.org/abs/2504.16054) 通过异构机器人数据、语义预测和非机器人数据联合训练，强调在未见家庭环境中的泛化及长时域操作。
- [π0.7](https://arxiv.org/abs/2604.15483) 进一步使用 demonstrations、失败轨迹、性能标签、子目标图像等多种 context，使 generalist policy 能够被条件化和操控。

这反映出一个重要变化：通用性不再仅由模型参数承载，也由 context、语言、记忆和性能条件共同决定。

更具体地说，VLA 的意义不是简单地把语言加入 policy input。它尝试统一三个过去相对分离的问题：

1. 视觉识别：环境中有什么、物体在哪里；
2. 语义推理：指令要求什么、当前子目标是什么；
3. 连续控制：机器人下一段动作应该如何生成。

但近期工作也显示，VLA 本身不是终点。一个可部署系统仍然需要处理记忆、失败检测、价值评估、不确定性、低层反馈和安全约束。因此更准确的理解是：VLA 正成为机器人系统的**通用策略主干和多模态接口**。

### 1.2 从行为克隆转向“预训练 + RL 后训练”

纯 imitation learning 能提供广泛技能，但通常继承示范数据的噪声、次优行为和覆盖不足。Levine 的近期工作明显加强了强化学习在部署阶段的作用：

- [The RL Token](https://arxiv.org/abs/2604.23073) 在预训练策略上加入较小的 actor–critic 接口，使机器人能够利用少量真实交互继续学习。
- [Semantic RL](https://arxiv.org/abs/2606.31958) 不直接在所有低层动作上进行强化学习，而是在语言或语义技能空间中优化已有技能的组合。
- [Q-Gradient-Guided Flow Policies](https://arxiv.org/abs/2606.11087) 用价值梯度在测试时引导 flow-based action policy，不必重新训练完整策略。

总体范式正在变成：

\[
\text{VLA/BC prior} + \text{value or reward feedback} + \text{online/post-training RL}.
\]

这里的重要变化是 RL 的位置发生了改变。传统 robot RL 试图从随机初始化或少量 demonstration 学会整个任务，真实样本成本很高；新的 RL 位于预训练之后，主要负责：

- 提高动作精度；
- 利用失败数据；
- 学习示范中没有覆盖的恢复行为；
- 适应具体硬件与动力学；
- 优化难以通过 supervised learning 表达的长时域目标。

这也解释了为什么 reward model、value function 和 verifier 会重新重要：如果没有可靠的评价信号，VLA 只能模仿“数据里出现过什么”，不能系统地判断“什么行为更好”。

### 1.3 Test-time learning 更多表现为 context、memory 和 policy steering

Levine 路线中的测试时学习不一定意味着在线更新全部网络参数。更常见的形式是：

- 从当前示范、失败或视频中获取 context；
- 检索长期记忆；
- 在语义技能空间中重新组合行为；
- 用价值函数在推理时修正动作分布。

[MEM](https://arxiv.org/abs/2603.03596) 将短视频经验与长期文本记忆结合，使机器人能够参考先前策略和任务经验，并在较长任务中进行 in-context adaptation。

因此，机器人中的 in-context learning 正逐渐从“输入几个示例”发展为一种完整的经验接口：示范、历史失败、语言总结、子目标和性能信息都可以成为 context。

这里需要区分三种不同的能力：

- **检索**：找到过去相似的任务经验；
- **组合**：根据当前目标重组已有技能；
- **真正适应**：产生训练数据中没有直接出现的新策略或更新内部模型。

近期系统往往能较好实现前两项，但第三项仍然是开放问题。判断机器人是否真正具有 ICL，不能只看它是否接受长 context，而要测试它是否能根据新示范改变策略规律，并在 context 移除后恢复原行为。

### 1.4 长时域任务依赖层级化和 action abstraction

长任务不能可靠地仅靠逐时刻动作生成完成。Levine 的近期路线越来越强调：

- 高层语义规划；
- temporally extended action chunks；
- 已有技能的组合；
- 局部反馈控制与全局记忆的分工。

这意味着未来 VLA 很可能不是单一频率、单一表示的端到端策略，而是一个多时间尺度系统。

对于长时域机器人任务，可以把系统分为三层：

| 层级 | 典型时间尺度 | 主要表示 |
|---|---|---|
| 任务层 | 数十秒至数分钟 | 语言目标、子任务图、长期记忆 |
| 技能层 | 数百毫秒至数秒 | action chunk、temporally extended skill、子目标状态 |
| 控制层 | 毫秒至数十毫秒 | joint command、torque、feedback control |

Levine 的语义技能组合和 action chunking 可以理解为试图在任务层与控制层之间建立一个更可靠的技能接口。

### 1.5 Reward、value 与 verifier 正成为 VLA 的第二条主干

通用策略给出“可能的动作”，但它不一定知道动作是否安全、是否可达、是否比其他候选更好。因此近期趋势是给生成式策略增加评价路径：

\[
\text{candidate generation} \rightarrow
\text{value/reward/verifier} \rightarrow
\text{selection or guidance}.
\]

这与 LLM 的 generator–verifier 结构类似，但机器人评价器还必须处理部分可观测性、接触动力学、执行误差与真实时间限制。Q-gradient guidance 的意义就在于，它把生成式 flow policy 与价值优化连接起来：策略保持多模态动作生成能力，价值函数则在推理时使样本朝更优方向移动。

### 1.6 失败数据正在从“需要清洗的噪声”变成监督信号

早期 imitation datasets 常常只保存成功 demonstrations；但真实部署的大多数数据包含不完美动作、部分完成、恢复和失败。π0.7 一类工作将性能标签、失败轨迹和不同质量的数据作为 context 或训练信号，说明研究重点正在从“只学专家行为”转向“理解行为质量”。

其潜在影响是：未来数据飞轮不需要等待人工重新标注完整示范，而可以利用部署日志产生 preference、reward、success detector、recovery demonstration 和 hard-negative data。

## 2. 与 VLA、RL、world model 和 test-time training 的关系

| 方向 | Levine 路线中的作用 |
|---|---|
| VLA | 通用策略和多模态知识的主体 |
| RL | 从“会做”提高到稳定、精确和可恢复 |
| In-context learning | 利用当前示范、历史和语义条件快速改变行为 |
| Test-time training | 更接近轻量在线适应、价值引导和记忆更新，而不是完整重训 |
| World model | 目前相对 policy-centric；预测模型更多作为评价、规划或数据生成的辅助组件 |
| Hierarchy | 在语言、子目标和技能层面对长时域行为进行组合 |

## 3. 对机器人与 AI 趋势的判断

1. **VLA 将成为机器人软件栈的基础模型，而不是完整系统。** 它还需要记忆、价值评价、安全验证、规划和低层控制。
2. **RL 正在重新进入真实机器人系统。** 重点不再是从零开始学习，而是对 foundation policy 进行低成本 post-training。
3. **测试时计算将进入连续控制。** 类似语言模型的 reranking、search 和 verifier，将以 value guidance、trajectory selection 和 skill composition 的形式出现。
4. **长时域泛化将依赖多时间尺度表示。** 语言目标、技能、action chunk 和关节控制会承担不同层次的预测与决策。
5. **真实部署数据会形成闭环。** 失败、恢复、人工修正和评价数据会持续反哺策略。
6. **策略生成与策略评价会逐渐分离。** 大型 VLA 负责提出行为，较小的 value/verifier 负责在线判断与修正。
7. **ICL、TTT 与 RL 的界限会变得模糊。** 未来系统可能先用 context 适应，再用 search 选择，最后只在高价值或高不确定性样本上更新参数。
8. **机器人 scaling law 不会只取决于模型规模。** 数据覆盖、动作表示、反馈质量、机器人在线时长和硬件异质性同样决定性能。

## 4. 与我的研究方向的连接

我的研究包括：physics-grounded human-motion prediction、uncertainty-aware prediction for crowd navigation，以及用于 humanoid 长时域任务的 action-conditioned skill-level world model。

与 Levine 路线最直接的结合点是：

- 将 skill-level world model 放在 VLA 与低层控制器之间；
- 让 VLA 提出语义子目标或候选技能；
- world model 预测技能执行后的状态、进度和失败模式；
- uncertainty estimator 判断预测是否可信；
- value/reward model 对候选技能排序；
- 只把局部执行交给高频反馈控制器。

一个适合的研究表述是：

> An uncertainty-aware, action-conditioned skill world model for planning and post-training generalist VLA policies on long-horizon humanoid tasks.

### 4.1 为什么 skill-level world model 与 Levine 路线互补？

VLA 的 action chunk 虽然减少了逐步生成开销，但它通常仍然直接预测动作序列，未必显式预测该技能执行后世界将变成什么样。Skill-level world model 可以补上这个缺口：

\[
p(z_{t+k}, o_{t+k}, y_{t+k}\mid z_t,o_t,\text{skill}_t),
\]

其中可以同时预测机器人状态、物体状态、任务进度以及 success/failure outcome。这样 VLA 的候选技能就能在执行前被想象、比较和验证。

### 4.2 不确定性应该放在哪里？

不确定性不应只作为 prediction interval 输出给用户，而应实际改变决策：

- 低不确定性：直接执行 VLA 候选技能；
- 中等不确定性：增加 world-model samples 或缩短 planning horizon；
- 高不确定性：调用更强模型、检索记忆、请求示范或进入安全控制；
- 明显 OOD：拒绝 imagined rollout 进入 RL replay buffer。

这可以把你在 crowd navigation 中积累的 online calibration 思想迁移到 VLA/world-model 系统。

### 4.3 Physics grounding 的作用

对于 humanoid，视觉上合理的未来不一定动力学可行。Physics grounding 可以作为：

- 模型结构中的 equivariance 或 contact representation；
- 训练损失中的 balance/contact/energy penalty；
- 推理时的 feasibility constraint；
- world-model rollout 后的 verifier。

其中，作为 verifier 尤其适合与 Levine 的 generator–value 路线结合，因为它不要求生成模型在内部完美学会所有物理规律，却能过滤明显不可执行的技能。

## 5. 与 Finn 和 Abbeel 的区别

- 相比 Chelsea Finn，Levine 更强调通用策略、规模化训练和完整机器人学习栈；Finn 更强调少样本适应、偏好和 world-model-assisted test-time decision making。
- 相比 Pieter Abbeel，Levine 更偏策略与学习算法；Abbeel 更强调 humanoid、dexterous manipulation、触觉、仿真和复杂 embodiment 的技能获取。

## 6. 后续更新时应追踪的问题

- VLA 的 RL post-training 是否能稳定扩展到多任务和长时间部署？
- flow policy 的 test-time value guidance 是否能满足真实机器人实时性？
- memory/context 是否产生真正的新策略，还是主要完成检索和模仿？
- generalist policy 与显式 world model 会融合，还是长期保持模块化？
- 技能级动作抽象能否降低长时域 world-model compounding error？

## 7. 完整讨论结论

Levine 的研究趋势不能简单概括为“做 VLA”。更完整的判断是：他正在构建一个以 generalist VLA 为中心、由记忆、语义技能、生成式动作模型、reward/value、RL post-training 与真实部署数据共同组成的机器人学习栈。

在这条路线中，ICL 主要负责利用上下文即时改变行为；test-time search/value guidance 负责在不重训大模型的情况下提升动作；RL 则负责将持续反馈固化为能力。World model 当前不是最中心的组件，但非常适合作为候选技能的预测器和 verifier 接入这一系统。

对我的研究而言，最有辨识度的位置不是再训练一个一般性的 VLA，而是研究：**如何用有物理结构、可校准且在技能时间尺度上进行预测的 world model，为 VLA 的长时域规划、测试时搜索和 RL 后训练提供可靠的中间模型。**
