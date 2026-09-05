# 论文主题分类表（项目统一 taxonomy）

所有研究者报告的论文分组都使用下面的类别 ID（与 `categories.json` 一致），这样不同研究者之间的图表和统计才能横向比较。每个类别给出：**它在研究什么、为什么重要、典型问题**。在报告中给每个类别加一段面向非专业读者的描述时，可直接改写这里的文字。

| ID | 中文名 | 英文名 |
|---|---|---|
| `generalist-vla` | 通用机器人基础模型（VLA） | Generalist VLA / robot foundation models |
| `chunking-realtime` | 动作分块与实时执行 | Action chunking & real-time execution |
| `rl-posttraining` | 真实机器人 RL 后训练 | Real-robot RL post-training |
| `test-time-steering` | 生成式策略的测试时引导与价值学习 | Test-time steering & value learning for generative policies |
| `reasoning-hierarchy-memory` | 具身推理、层级控制与记忆 | Embodied reasoning, hierarchy & memory |
| `eval-reward-data` | 评估、奖励模型与数据飞轮 | Evaluation, reward models & data flywheel |
| `scalable-value-learning` | 可扩展价值学习（算法基础） | Scalable value learning (RL foundations) |
| `llm-agent-rl` | LLM 与智能体 RL | LLM / agent RL |
| `world-model` | 世界模型与视频预测 | World models & video prediction |
| `humanoid-locomotion` | 人形与腿足运动控制 | Humanoid & legged locomotion |
| `dexterous-manipulation` | 灵巧操作与触觉 | Dexterous & tactile manipulation |
| `sim2real` | 仿真、sim-to-real 与数据生成 | Simulation, sim-to-real & data generation |
| `human-robot-interaction` | 人机交互与偏好学习 | Human-robot interaction & preferences |
| `other` | 其他 | Other |

需要新类别时：在 `categories.json` 中新增 ID、双语标签和颜色，并在本文件补一段描述；不要在单个报告里私自发明只用一次的类别。

---

## 各类别说明

### `generalist-vla` 通用机器人基础模型（VLA）

VLA = Vision-Language-Action，指一个把摄像头图像、自然语言指令直接映射为机器人动作的大模型，通常以预训练的视觉语言模型（VLM）为主干，再加一个动作输出头（离散 token、diffusion 或 flow）。这一类论文研究：如何用多机器人、多任务、乃至网络数据和人类视频训练**一个**策略；如何选择动作表示（tokenization vs 连续生成）；如何在加动作头时不破坏 VLM 的语义知识；以及这种模型能泛化到什么程度（新物体、新场景、新机器人）。相关数据集与开源模型（DROID、Octo、OpenVLA）也归入此类。

### `chunking-realtime` 动作分块与实时执行

Action chunking 指策略一次预测未来一段动作序列（如 50 步），而不是每个时间步只预测一个动作。它最初是模仿学习的工程技巧，现在成了独立研究对象：为什么它有效、如何把它带进 RL（在"chunk 空间"里学价值函数）、以及大模型推理延迟（几百毫秒）下如何平滑地边执行边生成下一段动作。这一类论文关注的是**控制频率与模型规模之间的矛盾**。

### `rl-posttraining` 真实机器人 RL 后训练

先用示范数据预训练（行为克隆 / VLA），再在真实机器人上用强化学习继续改进精度、速度和恢复能力。核心难点是样本效率与稳定性：真实机器人每小时只能采集有限数据。这类论文研究在哪个空间做 RL（原始动作、潜噪声、紧凑读出表征、语言 prompt）、如何设计奖励、如何让预训练策略成为好的 RL 初始化、以及如何在微调新任务时不丢失通用能力。

### `test-time-steering` 生成式策略的测试时引导与价值学习

现代机器人策略多为 diffusion / flow 生成模型，输出多模态的动作分布。这一类论文研究如何用一个**价值函数（Q 函数）**来改进这类策略——要么在训练时把价值梯度传回生成过程（困难，因为多步去噪反传不稳定），要么在测试时用价值对候选动作重排序或做梯度引导，而不重新训练策略。这与大语言模型里的"生成器 + 验证器"测试时计算是同一思路。

### `reasoning-hierarchy-memory` 具身推理、层级控制与记忆

机器人做长任务（几分钟到十几分钟）时，需要在行动前推理子目标（具身 chain-of-thought）、需要高层 VLM 与低层 VLA 之间有丰富的接口（不只是一句话指令，还包括子任务、运动描述、像素坐标、子目标图像），也需要多尺度记忆（短期视频记忆处理遮挡，长期文本记忆记住任务进度）。这类论文研究的是**如何组织一个多层级、有记忆、能在上下文中调整策略的系统**。

### `eval-reward-data` 评估、奖励模型与数据飞轮

通用策略要在很多任务和环境上评估，人工评估慢且贵。这类论文研究：自动化 / 分布式 / 仿真化的评估基础设施（AutoEval、RoboArena、real-to-sim、视频世界模型做评估器）；通用的视觉语言奖励模型（用 VLM 判断任务是否成功）；以及自主数据收集与自我改进流水线。它们共同构成"部署 → 评估 → 产生奖励/失败数据 → 再训练"的**数据飞轮**。

### `scalable-value-learning` 可扩展价值学习（算法基础）

基础 RL 算法研究：价值函数（Q / V）能否像语言模型那样随数据、算力、模型规模可预测地变好？包括用分类损失替代回归、UTD（更新次数/数据量比）与模型大小的算力分配、长 horizon 为何是离线 RL 扩展的障碍、目标条件 RL 的新价值更新规则、以及标准基准（OGBench）。这些工作为上面所有"用价值函数改进 generalist"的方法提供理论与经验基础。

### `llm-agent-rl` LLM 与智能体 RL

把 RL 用于大语言模型 / 多模态模型的智能体任务（多轮对话、网页与设备操作、数学推理）。虽然不直接涉及机器人，但方法论与机器人侧高度平行：RL 后训练 vs SFT 的泛化差异、验证器驱动的测试时计算、在语言空间做 actor-critic、自生成任务课程等。追踪它可以看到同一研究组在两个领域之间的思想迁移。

### `world-model` 世界模型与视频预测

学习一个预测"执行某动作后世界会变成什么样"的模型（像素级视频预测、潜空间动力学、技能级预测），用于规划、想象数据生成、策略评估或作为 verifier。相关研究者（如 Finn、Abbeel）在此类别上论文更多；Levine 组的世界模型工作多与评估或 model-based value expansion 相关。

### `humanoid-locomotion` 人形与腿足运动控制

双足 / 四足 / 人形机器人的运动控制，通常用大规模仿真 RL + sim-to-real，或从人类运动捕捉数据学习。关注鲁棒性、动态技能（跑、跳、恢复）、全身控制与运动-操作结合。

### `dexterous-manipulation` 灵巧操作与触觉

多指手、双臂、接触丰富的操作任务，以及触觉 / 力觉传感的使用。关注高精度、接触动力学、异构传感器融合。

### `sim2real` 仿真、sim-to-real 与数据生成

仿真环境构建、域随机化、real-to-sim 重建、用生成模型合成训练数据等。目的是用低成本数据替代或补充真实机器人数据。

### `human-robot-interaction` 人机交互与偏好学习

从人类反馈、偏好、纠正、语言指令中学习；人类意图推断；协作任务。关注如何让机器人行为符合人的期望并在交互中改进。

### `other`

不属于以上任何一类、但对理解研究者整体方向有用的论文（如优化器、科学设计、专利）。尽量少用。
