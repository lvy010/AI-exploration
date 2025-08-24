# E3NN 学习与测试项目

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.9.0%2B-red.svg)](https://pytorch.org/)
[![e3nn](https://img.shields.io/badge/e3nn-0.5.0%2B-green.svg)](https://e3nn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

本项目是一个全面的 **e3nn**（Euclidean Neural Networks）学习和测试套件，专注于演示等变神经网络的核心概念和实际应用。e3nn 是一个用于构建等变神经网络的 PyTorch 库，特别适用于需要保持旋转和反射对称性的任务。

## 🎯 项目目标

- **教育性**：通过详细的示例代码学习 e3nn 的核心概念
- **实用性**：提供可运行的测试代码验证等变性质
- **完整性**：覆盖 e3nn 的主要模块和功能
- **可扩展性**：为进一步的研究和开发提供基础

## 📁 项目结构

```
e3nn/
├── README.md                    # 项目文档（本文件）
├── requirements.txt             # 依赖包列表
├── run_all_tests.py            # 主测试运行脚本
├── test_e3nn_irrep.py          # 不可约表示测试
├── test_e3nn_gate.py           # 门控模块测试
└── test_e3nn_linear.py         # 线性层测试
```

## 🧩 核心模块测试

### 1. 不可约表示 (Irreducible Representations)
**文件**: `test_e3nn_irrep.py`

测试 e3nn 的基础概念——不可约表示（Irreps），包括：
- ✅ 基本 Irrep 对象的创建和属性
- ✅ 球谐函数的计算和可视化
- ✅ 复合 Irreps 的组合和操作
- ✅ 旋转群表示矩阵的生成
- ✅ 等变性验证

**关键特性**：
- 标量 (`0e`)、向量 (`1o`)、张量 (`2e`, `3o` 等) 的表示
- 宇称（偶/奇）的处理
- 旋转操作下的等变性验证

### 2. 门控模块 (Gate Module)
**文件**: `test_e3nn_gate.py`

演示 e3nn 的门控机制，用于非线性激活：
- ✅ 基本门控模块的使用
- ✅ 标量激活与向量门控的结合
- ✅ 复杂门控配置
- ✅ 等变性验证
- ✅ 手动计算与模块输出的对比

**关键特性**：
- 选择性激活不同类型的特征
- 保持旋转等变性的非线性操作
- 灵活的激活函数配置

### 3. 等变线性层 (Equivariant Linear Layer)
**文件**: `test_e3nn_linear.py`

测试 e3nn 的核心组件——等变线性变换：
- ✅ 基本线性层的创建和使用
- ✅ 复杂不可约表示的线性变换
- ✅ 严格的等变性数学验证
- ✅ 参数效率分析
- ✅ 不同宇称组合的处理

**关键特性**：
- 自动确保旋转等变性
- 参数高效的权重矩阵
- 灵活的输入输出配置

## 🚀 快速开始

### 环境要求

- Python 3.7+
- PyTorch 1.9.0+
- e3nn 0.5.0+
- NumPy 1.21.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

#### 运行所有测试
```bash
python run_all_tests.py
```

#### 运行单个测试模块
```bash
# 测试不可约表示
python test_e3nn_irrep.py

# 测试门控模块
python test_e3nn_gate.py

# 测试线性层
python test_e3nn_linear.py
```

## 📊 测试输出示例

### 不可约表示测试
```
=== 基本Irrep对象测试 ===
标量Irrep: 0e, l=0, p=1, 维度=1
矢量Irrep: 1o, l=1, p=-1, 维度=3

=== 球谐函数测试 ===
l=2的球谐函数在点(1,0,0): tensor([ 0.0000,  0.0000,  0.3154,  0.0000,  0.5000])
```

### 线性层等变性验证
```
等变性验证: True
✓ 线性层满足等变性！
参数效率: 62.50%
```

## 🔬 核心概念解释

### 等变性 (Equivariance)
如果一个函数 f 满足 `f(g·x) = g·f(x)`，其中 g 是群元素，则称 f 对群作用等变。在神经网络中，这意味着网络对输入的旋转/反射具有一致的响应。

### 不可约表示 (Irreducible Representations)
群的最小维数表示，不能进一步分解。在 e3nn 中，用于描述不同几何对象（标量、向量、张量）的变换行为。

### 门控机制 (Gating)
一种保持等变性的非线性激活方法，通过标量门控向量特征，实现选择性激活。

## 🎓 学习路径

1. **入门**：从 `test_e3nn_irrep.py` 开始，理解基本概念
2. **进阶**：学习 `test_e3nn_linear.py`，掌握线性变换
3. **高级**：探索 `test_e3nn_gate.py`，理解非线性操作

## 🛠️ 扩展开发

本项目为进一步的 e3nn 应用开发提供了坚实基础：

- **分子性质预测**：利用旋转等变性处理 3D 分子结构
- **点云处理**：对 3D 点云数据进行几何深度学习
- **物理系统建模**：保持物理对称性的神经网络
- **计算机视觉**：处理 3D 场景理解和重建

## 📚 参考资料

- [e3nn 官方文档](https://docs.e3nn.org/)
- [e3nn GitHub 仓库](https://github.com/e3nn/e3nn)
- [论文: "e3nn: A modular framework for equivariant neural networks"](https://arxiv.org/abs/2207.09453)
- [球谐函数理论](https://en.wikipedia.org/wiki/Spherical_harmonics)

## 🤝 贡献指南

欢迎提交 Issues 和 Pull Requests 来改进本项目：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢 [e3nn 团队](https://e3nn.org/) 开发了这个优秀的等变神经网络库
- 感谢 PyTorch 社区提供的深度学习框架支持

---

**注意**：本项目主要用于教育和研究目的。在生产环境中使用前，请确保充分测试和验证。

如有任何问题或建议，请随时联系或提交 Issue！
