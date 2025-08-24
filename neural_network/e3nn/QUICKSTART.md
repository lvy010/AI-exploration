# E3NN 快速入门指南

## 5分钟上手 e3nn

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行第一个测试
```bash
python test_e3nn_irrep.py
```

### 3. 核心概念速览

#### 不可约表示 (Irreps)
```python
from e3nn.o3 import Irrep, Irreps

# 创建单个不可约表示
scalar = Irrep("0e")    # 标量
vector = Irrep("1o")    # 向量

# 创建组合表示
irreps = Irreps("2x0e + 1x1o")  # 2个标量 + 1个向量
print(f"总维度: {irreps.dim}")   # 输出: 5
```

#### 等变线性层
```python
from e3nn.o3 import Linear

# 创建等变线性层
layer = Linear(
    irreps_in="1x0e + 1x1o",    # 输入: 1标量 + 1向量
    irreps_out="2x0e + 1x1o"    # 输出: 2标量 + 1向量
)

# 使用
x = irreps_in.randn(batch_size, -1)
y = layer(x)  # 自动保持旋转等变性！
```

#### 门控激活
```python
from e3nn.nn import Gate

gate = Gate(
    irreps_scalars="1x0e",      # 直接激活的标量
    act_scalars=[torch.tanh],   # 激活函数
    irreps_gates="1x0e",        # 门控标量
    act_gates=[torch.sigmoid],  # 门控激活函数
    irreps_gated="1x1o"         # 被门控的向量
)
```

### 4. 验证等变性
```python
import torch
from e3nn import o3

# 创建随机旋转
R = o3.rand_matrix()

# 测试: f(Rx) = Rf(x)
x_rotated = irreps_in.D_from_matrix(R) @ x.T
y1 = layer(x_rotated.T)

y = layer(x)
y2 = irreps_out.D_from_matrix(R) @ y.T

# 验证等变性
assert torch.allclose(y1, y2.T, atol=1e-6)
print("✅ 等变性验证通过！")
```

### 5. 完整示例运行
```bash
# 运行所有测试
python run_all_tests.py

# 单独运行特定模块
python test_e3nn_linear.py    # 线性层测试
python test_e3nn_gate.py      # 门控模块测试
```

## 常见问题

**Q: 什么是等变性？**
A: 等变性意味着网络对输入的几何变换具有一致的响应。如果输入旋转，输出也会相应旋转。

**Q: e3nn适用于什么场景？**
A: 分子性质预测、3D点云处理、物理系统建模等需要几何对称性的任务。

**Q: 如何选择合适的Irreps？**
A: 根据数据的几何性质选择：标量用0e，向量用1o，高阶张量用2e、3o等。

## 下一步

- 阅读完整的 [README.md](README.md)
- 查看 [e3nn官方文档](https://docs.e3nn.org/)
- 尝试修改测试代码中的参数
