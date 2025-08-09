# CUTLASS GEMM 示例

这个项目演示了如何使用NVIDIA CUTLASS库实现高性能的GEMM（General Matrix Multiply）操作。

## 功能特性

- 高度模板化的CUTLASS GEMM实现
- 支持多种数据类型（float、half、int8等）
- 可配置的矩阵布局（行优先/列优先）
- 针对不同GPU架构优化
- 包含CPU参考实现用于验证
- 提供多个示例版本（CUTLASS、简单CUDA、CPU）

## 系统要求

- NVIDIA GPU（支持CUDA）
- CUDA Toolkit 11.0或更高版本
- CUTLASS库
- C++17兼容的编译器

## 安装依赖

### 1. 安装CUDA Toolkit

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nvidia-cuda-toolkit

# 或者从NVIDIA官网下载安装
# https://developer.nvidia.com/cuda-downloads
```

### 2. 安装CUTLASS

```bash
# 方法1：从GitHub克隆
git clone https://github.com/NVIDIA/cutlass.git
cd cutlass
mkdir build && cd build
cmake .. -DCUTLASS_NVCC_ARCHS=80  # 根据你的GPU调整架构
make -j$(nproc)
sudo make install

# 方法2：使用conda（推荐）
conda install -c conda-forge cutlass
```

## 项目结构

```
cuda-cutlass/
├── gemm_example.cpp           # CUTLASS GEMM示例（完整版）
├── simple_gemm_example.cpp    # 简单CUDA GEMM示例
├── cpu_gemm_example.cpp       # CPU GEMM示例（演示概念）
├── CMakeLists.txt             # CMake构建配置
├── Makefile                   # Makefile构建配置
├── README.md                  # 说明文档
└── cutlass/                   # CUTLASS库（本地克隆）
```

## 构建项目

### 使用Makefile（推荐）

```bash
# 检查环境
make check-env

# 构建所有示例
make all

# 或者构建特定示例
make gemm_example           # CUTLASS版本
make simple_gemm_example    # 简单CUDA版本
make cpu_gemm_example       # CPU版本
```

### 使用CMake

```bash
mkdir build
cd build
cmake ..
make -j$(nproc)
```

## 运行示例

### 1. CPU版本（推荐用于测试）

```bash
# 构建并运行CPU版本
make cpu_gemm_example
./cpu_gemm_example
```

这个版本演示了CUTLASS的模板化概念，不需要GPU即可运行。

### 2. 简单CUDA版本

```bash
# 构建并运行简单CUDA版本
make simple_gemm_example
./simple_gemm_example
```

这个版本使用cuBLAS进行GEMM计算，需要CUDA环境。

### 3. CUTLASS版本

```bash
# 构建并运行CUTLASS版本
make gemm_example
./gemm_example
```

这个版本使用完整的CUTLASS库，需要正确配置的CUTLASS环境。

## 示例输出

### CPU版本输出示例

```
=== CUTLASS风格GEMM示例（CPU版本）===

矩阵维度: M=256, N=256, K=128
矩阵初始化完成
初始化GEMM配置:
  Threadblock形状: 128x128x8
  Warp形状: 32x64x8
GEMM初始化成功
执行GEMM操作: C = 1 * A * B + 0 * C
GEMM执行完成
计算参考结果...
验证结果...
✓ GEMM测试通过！结果正确。

=== 结果统计 ===
矩阵A维度: 256x128
矩阵B维度: 128x256
矩阵C维度: 256x256
总计算量: 16777216 次浮点运算

=== 性能基准测试 ===
矩阵维度: 256x256x128
迭代次数: 5
总执行时间: 0.07 秒
平均执行时间: 0.01 秒
性能: 1.13 GFLOPS
```

## 关键代码解释

### 1. CUTLASS模板化结构

```cpp
// 定义数据类型和布局
using ElementA = float;
using ElementB = float;
using ElementC = float;
using LayoutA = cutlass::layout::ColumnMajor;
using LayoutB = cutlass::layout::RowMajor;
using LayoutC = cutlass::layout::ColumnMajor;

// 定义GPU架构和性能参数
using ArchTag = cutlass::arch::Sm80;
using ThreadblockShape = cutlass::gemm::GemmShape<128, 128, 8>;
using WarpShape = cutlass::gemm::GemmShape<32, 64, 8>;
```

### 2. GEMM内核实例化

```cpp
using Gemm = cutlass::gemm::device::Gemm<
    ElementA, LayoutA,
    ElementB, LayoutB,
    ElementC, LayoutC,
    ElementAccumulator,
    OpClass,
    ArchTag,
    ThreadblockShape,
    WarpShape,
    InstructionShape,
    EpilogueOutputOp,
    cutlass::gemm::threadblock::GemmIdentityThreadblockSwizzle<>,
    2
>;
```

### 3. 执行GEMM操作

```cpp
// 创建GEMM参数
typename Gemm::Arguments arguments(
    {M, N, K},
    tensor_A.device_ref(),
    tensor_B.device_ref(),
    tensor_C.device_ref(),
    tensor_C.device_ref(),
    {alpha, beta}
);

// 执行GEMM
Gemm gemm_op;
gemm_op.initialize(arguments);
gemm_op(arguments);
```

## 性能优化

1. **线程块尺寸**：根据GPU架构调整`ThreadblockShape`
2. **Warp尺寸**：优化`WarpShape`以提高并行效率
3. **数据类型**：使用`half`或`int8`可以获得更好的性能
4. **Tensor Core**：对于支持的GPU，使用`OpClassTensorOp`

## 故障排除

### 常见问题

1. **CUTLASS未找到**
   ```bash
   export CUTLASS_ROOT=/path/to/cutlass
   ```

2. **CUDA架构不匹配**
   - 检查你的GPU架构：`nvidia-smi`
   - 更新`CMAKE_CUDA_ARCHITECTURES`或`-arch=sm_XX`

3. **编译错误**
   - 确保使用C++17或更高版本
   - 检查CUDA和CUTLASS版本兼容性

4. **GPU不可用**
   - 使用CPU版本进行测试：`make test-cpu`
   - 检查CUDA环境：`nvcc --version`

### 调试模式

```bash
# 使用CMake调试模式
cmake -DCMAKE_BUILD_TYPE=Debug ..
make

# 使用Makefile调试模式
make NVCC_FLAGS="-g -G" all
```

## 扩展功能

- 支持更多数据类型（bfloat16、int8等）
- 添加性能基准测试
- 实现更复杂的尾声操作
- 支持批量GEMM操作
- 添加更多矩阵布局支持

## 参考资料

- [CUTLASS官方文档](https://github.com/NVIDIA/cutlass)
- [CUDA编程指南](https://docs.nvidia.com/cuda/)
- [NVIDIA开发者论坛](https://forums.developer.nvidia.com/)
- [CUTLASS论文](https://arxiv.org/abs/1810.07831) 