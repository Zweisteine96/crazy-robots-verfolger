# 1H · LLM / 智能体 RL（AI 侧的平行线）

> 所属报告：[Sergey Levine 近期研究趋势分析](../Sergey_Levine.md) · 类别 ID：`llm-agent-rl` · 论文数：11（2024: 3 / 2025: 7 / 2026: 1）  
> 所有链接均为 arXiv 摘要页，已通过 `verify_links.py` 核对。

---

## 1. 这个方向在研究什么

把强化学习用于大语言模型（LLM）和多模态模型（VLM）的**智能体**任务：多轮对话、网页浏览、手机 / 设备操作、工具使用、数学推理。这些任务与机器人的共同点是：需要在多步交互中做决策、奖励往往稀疏且在最后才来、探索空间巨大。

这一类论文关心：

1. **多轮 RL**：现有 LLM 的 RL 多为单轮（一个 prompt → 一个回答 → 一个奖励）。多轮任务如何做信用分配（ArCHer、NLAC）？
2. **从自主经验学习**：能否不用人工标注的示范，让 agent 在真实网页 / 设备上自己练（DigiRL、Digi-Q、PAE、Self-Challenging）？
3. **RL vs SFT 的泛化**：同样的数据，RL 后训练和监督微调谁更能泛化到分布外（SFT Memorizes, RL Generalizes）？
4. **测试时计算**：多想一会儿、多采几个样是否有用？有验证器和没验证器有什么区别（Scaling TTC Without Verification、ZIP）？
5. **奖励从哪里来**：没有可验证答案时，能否用模型自身的信号（Intuitor）或隐式价值（VIMPO）？

**为什么放进机器人报告**：Levine 组同时在两个领域工作，很多结论互为镜像——RL 后训练更泛化、验证器驱动的测试时计算更优、在结构化中间空间做 RL 更高效。把这一类别与 1C / 1D 对照阅读，可以看到方法论是如何在两个领域之间迁移的。2025 年该类别 7 篇，是本报告中仅次于 VLA 的高产方向。

---

## 2. 论文逐篇分析（按时间）

### 2024

**[ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL](https://arxiv.org/abs/2402.19446)**（2024-02）  
LLM 的 agent 任务（网页、工具、客服）需要在多轮交互中决策，但现有 RL 方法几乎都优化单轮奖励，因此无法让 LLM 跨轮次搜集信息、做信用分配、反思过去动作。ArCHer 采用**层级 RL**：并行运行两个 RL 算法——高层的离策略价值 RL 在"话语"级别聚合奖励，低层 RL 利用高层价值函数在每轮话语内训练 token 策略。保留了单轮 RL 方法（如 PPO）的灵活性，同时处理多轮、长 horizon、延迟奖励。样本效率比现有方法高约 **100 倍**，并随模型容量（测到 7B）提升。**意义**：本类别起点。"高层价值在粗时间尺度、低层策略在细时间尺度"与机器人侧 Decoupled Q-Chunking（1B）的结构完全平行。

**[DigiRL: Training In-The-Wild Device-Control Agents with Autonomous RL](https://arxiv.org/abs/2406.11896)**（2024-06）  
VLM 训练语料缺少决策数据，在真实 GUI 上做设备控制时表现差；静态示范训练无法应对真实世界的随机性与非平稳性。DigiRL 两阶段：离线 RL 初始化 → offline-to-online RL；构建可扩展的并行 Android 学习环境（带 VLM 评估器），用优势加权 RL（优势估计考虑随机性）加自动课程。1.3B VLM 在 Android-in-the-Wild 上成功率从 17.7% 提升到 67.2%（比 SFT 高 49.5 个百分点），超过 GPT-4V 的 AppAgent（8.3%）、17B CogAgent（38.5%）和此前最佳自主 RL 方法（57.8%）。**意义**：机器人 RL 的"离线预训练 + 在线微调 + 自动奖励"配方直接迁移到数字 agent。

**[PAE: Proposer-Agent-Evaluator — Autonomous Skill Discovery for Foundation Model Internet Agents](https://arxiv.org/abs/2412.13194)**（2024-12）  
通用 agent（互联网浏览 agent、家用人形机器人）需要大而多样的技能库，若每个技能都要人工标注指令，技能库必然受限。PAE 让基础模型 agent 在野外**自主发现并练习技能**：上下文感知的任务提议者根据环境信息（用户示范、甚至只是网站名）提出任务；agent 尝试；VLM 成功评估器给出奖励；RL 精炼策略。在 WebVoyager、WebArena 的真实与自托管网站上验证，据其所知是第一个用自主任务提议 + RL 并在人工标注基准上达到 SOTA 的学习系统。**意义**：与机器人侧 AutoRT / SOAR（1F）同构——用基础模型提任务、评成败，形成自主数据飞轮。

### 2025

**[SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-training](https://arxiv.org/abs/2501.17161)**（2025-01）  
用 GeneralPoints（算术推理卡牌游戏）与 V-IRL（真实世界导航）研究 SFT 与 RL 在文本规则变体与视觉变体上的泛化。结论：**RL（尤其用结果奖励训练）在文本与视觉变体上都泛化；SFT 倾向记忆训练数据、难以泛化到分布外**。RL 还提升了模型的底层视觉识别能力。但 SFT 对有效的 RL 训练仍然必要——它稳定输出格式，使后续 RL 能取得收益。**意义**：为整个"预训练 + RL 后训练"范式提供了一个干净的对照实验，其结论与机器人侧 RLDG（RL 数据优于人类示范）、π\*0.6 一致。

**[Digi-Q: Learning Q-Value Functions for Training Device-Control Agents](https://arxiv.org/abs/2502.15760)**（2025-02）  
在设备控制这类开放 agent 任务中，每次真实交互都有成本，on-policy RL 不理想；能利用离策略经验的 Q 函数更有效。Digi-Q 在**冻结的 VLM 中间层特征**上用离线 TD 学习训练 Q 函数（比微调整个 VLM 省算力、更可扩展），先用一个初始微调阶段放大特征中的可操作信息；训练好后用 **Best-of-N 策略提取**——从当前策略的多个候选动作中按价值挑最好的来模仿——无需环境交互即可改进策略。在 Android-in-the-Wild 上比此前最佳提升 21.2%，部分情况匹配需要交互的 SOTA RL。**意义**：与机器人侧 V-GPS（1D，价值重排序）和 RL Token（1C，在紧凑表征上训练价值头）同构。

**[Scaling Test-Time Compute Without Verification or RL is Suboptimal](https://arxiv.org/abs/2502.12118)**（2025-02）  
测试时计算有两种扩展方式：蒸馏成功的搜索 / 思考轨迹（无验证器，VF），或用验证（0/1 结果奖励、奖励模型、验证器）引导 RL 与搜索（有验证器，VB）。论文**证明**在固定算力 / 数据预算下，VB 方法远优于 VF；且当基座 LLM 对正确解轨迹呈异质分布（不同长度、风格）并且奖励分布不尖锐时（用反集中性形式化），随测试时算力与数据扩展，VF 的次优性扩展得很差，VB 渐近更好、差距随预算增长。在 3B / 8B / 32B 模型的数学推理上验证。**意义**：为机器人侧"生成 + 价值验证"（V-GPS、QGF）优于"只模仿更多数据"提供了理论支撑。

**[Intuitor: Learning to Reason without External Rewards](https://arxiv.org/abs/2505.19590)**（2025-05）  
RLVR（可验证奖励 RL）有效但依赖昂贵的领域监督。提出 RLIF（从内部反馈的 RL）：Intuitor 用模型自身的置信度——**self-certainty**——作为唯一奖励，替换 GRPO 中的外部奖励，实现完全无监督学习。在数学基准上匹配 GRPO，在代码生成等域外任务上泛化更好，且不需要标准答案或测试用例。**意义**：Scholar 引用 197 次。它探索了"没有可验证奖励时怎么办"，与机器人侧 Success Visitation Matching（从自身成败历史造奖励）的动机相同。

**[Self-Challenging Language Model Agents](https://arxiv.org/abs/2506.01716)**（2025-06）  
训练工具使用 agent 需要人工创建多样任务、工具与评估标准。Self-Challenging 框架让 agent **自己生成高质量任务**：先扮演挑战者，与工具交互后生成任务——形式为 Code-as-Task（指令 + 验证函数 + 解与失败样例作为测试），据此过滤高质量任务；再扮演执行者，用评估反馈作奖励做 RL。在 M3ToolEval 与 TauBench 上让 Llama-3.1-8B-Instruct 提升两倍以上，只用自生成数据。**意义**：PAE 的升级——任务本身带可执行的验证器，使奖励可靠。

**[NLAC: Natural Language Actor-Critic — Scalable Off-Policy Learning in Language Space](https://arxiv.org/abs/2512.04601)**（2025-12）  
长 horizon 稀疏奖励下，从轨迹级奖励学习噪声大、不稳定、样本复杂度高；在自然语言动作空间中靠随机探索发现更好动作很难。NLAC 用一个**生成自然语言而非标量的 LLM critic**：对为什么某动作次优给出语言解释，为 LLM 策略提供更丰富、可操作的训练信号——尤其在大而开放的动作空间中，无需随机探索即可推理如何改进。可离策略训练、无需策略梯度，更数据高效、更稳定。在推理、网页浏览、工具使用与对话任务上超过现有方法。**意义**：与机器人侧 SARL（1C，在 prompt 空间做 RL）互为镜像——两者都把 RL 的"评价"或"动作"搬进语言空间以获得结构化探索。

**[ZIP-RC: Zero-Overhead Introspection for Adaptive Test-Time Compute](https://arxiv.org/abs/2512.01457)**（2025-12）  
LLM 缺乏自省：不能预判自己会否成功、需要多少算力。Best-of-N 等方法用固定预算，不管每个样本的边际收益；学到的验证器能给置信度但不支持自适应推理且需额外模型。ZIP-RC 在同一次前向中**复用保留 / 未用的 logits**，在每个 token 输出"最终奖励 × 剩余长度"的联合分布——无额外模型、不改架构、零推理开销。用该分布计算采样效用（期望最大奖励、总算力、延迟的线性组合），推理时用元动作决定从哪个前缀继续或重新采样。在混合难度数学基准上比多数投票准确率高最多 12%（同等或更低成本），并描绘出质量—算力—延迟的平滑 Pareto 前沿。**意义**：这是"不确定性驱动的算力分配"在 LLM 侧的实现，与我关于 world model 不确定性决定采样量的设想同构。

### 2026

**[VIMPO: Value-Implicit Policy Optimization for LLMs](https://arxiv.org/abs/2606.20008)**（2026-06）  
RLVR 面临简单性与信用分配的权衡：GRPO 等组相对方法不需 critic，但给每个 token 相同的轨迹级优势；actor–critic 有稠密信号，但价值函数训练不稳定。VIMPO 是 **critic-free** 的策略优化：从 KL 正则化 RL 的最优性条件推导出"策略隐含的价值函数"，对自回归生成可写成策略—参考对数比的递推，以"轨迹末尾无剩余奖励"为锚。得到一个简单的价值损失（纳入结果级可验证奖励、无需训练 critic）和 critic-free 的 actor 优势，把奖励纳入（价值损失）与策略改进（PPO 式 actor 更新）分离。在 MATH-500、AIME 2024/2025、OlympiadBench 上超过 GRPO，竞赛式评测增益更大；噪声奖励下保持优势。**意义**：机器人侧 CFGRL（1D，不学价值函数也能做策略改进）的 LLM 对应物。

---

## 3. 演进脉络

```
2024-02  ArCHer            多轮层级 RL，100× 样本效率                 ← 多轮 RL
2024-06  DigiRL            离线 → 在线 RL 训练设备控制 agent          ← 自主经验
2024-12  PAE               提议者—执行者—评估者，自主技能发现
2025-01  SFT vs RL         RL 泛化、SFT 记忆                          ← 后训练范式对照
2025-02  Digi-Q            冻结特征上学 Q，Best-of-N 提取策略
2025-02  Scaling TTC       验证器驱动的测试时计算理论上更优           ← 测试时计算
2025-05  Intuitor          self-certainty 作唯一奖励                   ← 无外部奖励
2025-06  Self-Challenging  自生成带验证器的任务
2025-12  NLAC              语言空间的 actor–critic
2025-12  ZIP-RC            零开销自省，自适应算力
2026-06  VIMPO             critic-free 的隐式价值
```

---

## 4. 深度分析：与机器人侧的镜像对照

| 主题 | LLM 侧（1H） | 机器人侧 | 共同结论 |
|---|---|---|---|
| RL 后训练 vs 模仿 | SFT Memorizes, RL Generalizes | RLDG、π\*0.6 | RL 后训练更泛化；SFT / BC 仍是必要的初始化 |
| 层级时间尺度 | ArCHer（话语级价值 + token 级策略） | Decoupled Q-Chunking、SARL | 价值在粗尺度、策略在细尺度 |
| 价值重排序提取策略 | Digi-Q 的 Best-of-N | V-GPS | 价值函数可作为策略无关的外挂 |
| 在紧凑表征上学价值 | Digi-Q（冻结 VLM 特征） | RL Token | 不动主干，只训小头 |
| 验证器 vs 蒸馏 | Scaling TTC Without Verification | QGF 的测试时价值引导 | 有验证器的测试时计算更可扩展 |
| 无外部奖励 | Intuitor（self-certainty） | Success Visitation Matching | 从模型 / 历史内部造奖励 |
| 自主任务与评估 | PAE、Self-Challenging | AutoRT、SOAR、RoboReward | 基础模型提任务 + 评成败 = 数据飞轮 |
| 语言空间的 RL | NLAC（语言 critic） | SARL（prompt 空间 RL） | 语言是结构化探索的好空间 |
| 不学显式价值 | VIMPO | CFGRL | 策略改进可不依赖显式 critic |
| 自适应算力 | ZIP-RC | （尚无直接对应） | 不确定性决定采样 / 引导预算 |

**观察一**：几乎每一个机器人侧的方法都能在 LLM 侧找到对应，且时间上常常是 LLM 侧略早（Digi-Q 2025-02 → RL Token 2026-04；NLAC 2025-12 → SARL 2026-06）。个人推断：Levine 组把 LLM 作为"便宜的试验场"，验证的机制再迁到昂贵的机器人上。

**观察二**：唯一没有机器人对应的是 ZIP-RC 的自适应算力分配——这恰好是不确定性感知的 world model 可以填补的位置。

**观察三**：LLM 侧的"验证器"通常是离散的、事后的（答案对不对）；机器人侧的价值函数必须是连续的、逐步的。因此机器人侧更依赖梯度引导（QGF）而非重排序。

---

## 5. 与其他类别的连接

- ↔ **1C**：SFT vs RL、Digi-Q、NLAC 分别对应 RLDG / π\*0.6、RL Token、SARL。
- ↔ **1D**：Scaling TTC、Digi-Q、VIMPO 对应 QGF、V-GPS、CFGRL。
- ↔ **1F**：PAE、Self-Challenging 的 VLM 评估器对应 RoboReward、AutoRT、SOAR。
- ↔ **1G**：Digi-Q、VIMPO 是价值学习在语言模型上的变体。
- ↔ **1B**：ArCHer 的层级时间尺度对应 Decoupled Q-Chunking。

---

## 6. 与我的研究方向的连接

- **ZIP-RC 是"不确定性驱动算力分配"的现成范本**：它在同一次前向中预测奖励与剩余成本，并据此决定继续 / 重采样。skill-level world model 可以扮演同样的角色——预测每个候选技能的成功概率与执行成本，决定是否多采样、多引导或求助更强模型。
- **Scaling TTC 的理论**支持"world model 作为 verifier"的定位：有验证器的测试时计算渐近优于无验证器；world model + physics verifier 就是机器人侧的验证器。
- **Intuitor 的 self-certainty 奖励**提示：world model 自身的预测置信度也可以作为一种内部奖励 / 探索信号，用于在没有外部成功检测的任务中引导 RL。
- **NLAC 的语言 critic**——"解释为什么次优"——对 humanoid 长时域任务的失败诊断有借鉴意义：world model 预测的失败模式若能以语言形式反馈给高层规划器（如 LITEN 的上下文），比标量价值更可操作。

---

## 7. 待追踪问题

- ZIP-RC 式的自省能否迁到 VLA（预测"这个动作块会不会成功、还要多久"）？
- LLM 侧的 critic-free 方法（VIMPO）会否影响机器人侧对显式价值函数的依赖？
- Self-Challenging 的"带验证器的自生成任务"能否用于机器人（任务 + 自动成功检测器）？
- 两侧的方法迁移是否会反向——机器人侧的连续价值梯度引导（QGF）用于 LLM 的连续潜空间推理？
