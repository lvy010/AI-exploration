# AI-exploration

> AI 各方向的初步探索与实践——跑通、改造、写教程，记录从系统底层转向 AI 的过程。

[linux-lab](https://github.com/lvy010/linux-lab)

这个仓库是我转向 AI 后的实验场：每个子项目对某个 AI 方向的动手探索，包括跑通开源项目、改造和微调、以及基于实践写成的教程。

---

## 项目

| Project | Description | Tags |
|---|---|---|
| [WeChat AI Bot](./ai-wechat/) | Integrating AI capabilities into WeChat messaging | `chatbot` `wechat` `llm` |
| [AI Image Story Generator](./AI_image/1Prompt1Story/) | Generate story images from a single prompt | `image-generation` `prompt` `stable-diffusion` |
| [Bubbles](./Bubbles) | Bubble animation / simulation experiment | `animation` `visualization` |
| [Robotics Exploration](./Robotics/) | Robotics-related AI experiments and simulations | `robotics` `simulation` |
| [AI Agent Builder](./agent_build/) | Building and testing autonomous AI agents | `agent` `llm` `openai` |
| [CUDA / CUTLASS GEMM Test](./cuda-cutlass/) | High-performance matrix multiplication with CUDA & CUTLASS | `cuda` `cutlass` `gemm` `c++` |
| [E3NN — Equivariant Neural Network](./neural_network/e3nn/) | Exploring E(3)-equivariant neural networks for 3D data | `e3nn` `neural-network` `3d` `pytorch` |
| [Pyro — Probabilistic Programming](./probability/pyro-code/) | Probabilistic modeling and inference using Pyro | `pyro` `probabilistic` `bayesian` `pytorch` |
| [RAGAS RAG Evaluation](./ragas_evaluation_demo/) | Evaluating RAG pipelines using the RAGAS framework | `rag` `evaluation` `ragas` `llm` |

---

## 技术栈

![Python](https://img.shields.io/badge/Python-82%25-blue)
![C++](https://img.shields.io/badge/C++-14%25-orange)
![CUDA](https://img.shields.io/badge/CUDA-GPU-green)

---

## 项目与文章

现在还是很完全，Notes after 7月2025日 (in progress): lvynote.github.io待整合加入

### Agent 构建（`agent_build/`）

基于 OpenAI 官方 [Building Effective Agents](./building-agents.pdf) 的系统性教程，从理论到代码：

- **设计基础**：模型选择策略、工具类型（数据/操作/编排）、指令设计
- **编排模式**：单 Agent 运行循环、Manager 模式、去中心化 Handoff 模式
- **安全护栏**：相关性分类器、PII 过滤、工具安全校验

可运行示例：天气查询 Agent → 多语言翻译 Manager → 客户流失检测护栏

配套文章：[设计基础](./agent_build/docs/agent_foundations.md) · [编排模式](./agent_build/docs/orchestration_patterns.md) · [安全护栏](./agent_build/docs/guardrails.md) · [学习路线](./agent_build/LEARNING_GUIDE.md)

### RAGAS RAG 评估（`ragas_evaluation_demo/`）

RAGAS 框架实战：端到端评估 RAG 管线的忠实度和答案相关性，含自定义 API 端点适配（支持国内代理）和测试集自动生成。

配套文章：[使用教程](./ragas_evaluation_demo/README.md) · [运行总结](./ragas_evaluation_demo/运行总结.md)

### GPU 计算（`cuda-cutlass/`）

从 CPU 到 GPU 的矩阵乘法性能对比教程：

- `cpu_gemm_example.cpp`：模板化 CPU GEMM，理解 CUTLASS 抽象
- `simple_gemm_example.cpp`：cuBLAS 版本
- `gemm_example.cpp`：完整 CUTLASS 模板 GEMM

配套文章：[教程](./cuda-cutlass/README.md) · [项目总结](./cuda-cutlass/SUMMARY.md)

### 几何深度学习（`neural_network/e3nn/`）

E(3) 等变神经网络的学习与验证套件，覆盖 e3nn 库核心概念：

- 不可约表示（Irreps）的创建、性质、张量积
- 等变线性层的严格等变性验证
- 门控机制的手动计算对照

配套文章：[教程](./neural_network/e3nn/README.md) · [快速入门](./neural_network/e3nn/QUICKSTART.md)

### 概率编程（`probability/pyro-code/`）

用 Pyro 做硬币偏置的贝叶斯推断：SVI + 先验敏感性分析 + 后验可视化。

配套文章：[教程](./probability/pyro-code/README.md)

### AI 图像故事生成（`AI_image/1Prompt1Story/`）

滑动窗口 Stable Diffusion 故事生成器：保持叙事连贯性的多帧图像生成。

配套文章：[教程](./AI_image/1Prompt1Story/README.md)

### 机器人运动仿真（`Robotics/`）

自行车模型运动学仿真：加速/转弯/减速多模式轨迹分析。

配套文章：[教程](./Robotics/README.md)

---

## 使用方式

各子目录独立，进入后按 README 操作：

```bash
# Agent 示例
cd agent_build && pip install -r requirements.txt
python examples/single_agent/weather_agent.py

# CUDA GEMM
cd cuda-cutlass && make cpu_gemm && ./cpu_gemm

# E3NN 测试
cd neural_network/e3nn && pip install -r requirements.txt
python run_all_tests.py

# RAG 评估
cd ragas_evaluation_demo && pip install -r requirements.txt
python ragas_demo.py
```

---

## 相关仓库

| 仓库 | 说明 |
|------|------|
| [linux-lab](https://github.com/lvy010/linux-lab) | Linux 系统方向：OSTEP 笔记、内核实验、50+ 篇专栏代码 |
| [nanoaios](https://github.com/lvy010/nanoaios) | 面向 Agent 时代的极简 AIOS 内核（Rust） |
| [X-Plore](https://github.com/lvy010/X-Plore) | 1500+ 篇博客专栏索引 |
| [Algo-Atlas](https://github.com/lvy010/Algo-Atlas) | 算法学习笔记与代码库 |

## 许可协议

MIT

