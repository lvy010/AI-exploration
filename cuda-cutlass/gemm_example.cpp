#include <cutlass/cutlass.h>
#include <cutlass/gemm/device/gemm.h>
#include <cutlass/util/host_tensor.h>
#include <cutlass/util/reference/host/tensor_fill.h>
#include <cutlass/util/reference/host/gemm.h>
#include <cutlass/util/reference/host/tensor_compare.h>

#include <iostream>
#include <cstdlib>

int main() {
    std::cout << "CUTLASS GEMM 示例开始..." << std::endl;

    // 1. 定义GEMM问题：C = alpha * A * B + beta * C
    // 选择简单的float类型GEMM
    using ElementA = float;
    using ElementB = float;
    using ElementC = float;
    using ElementAccumulator = float; // 内部累加器类型

    // 定义矩阵布局：A列优先，B行优先，C列优先
    // 对应传统BLAS中的'TN'操作（A转置，B不转置）
    using LayoutA = cutlass::layout::ColumnMajor;
    using LayoutB = cutlass::layout::RowMajor;
    using LayoutC = cutlass::layout::ColumnMajor;

    // 定义GPU架构（如NVIDIA Ampere架构）
    using ArchTag = cutlass::arch::Sm80; // 适用于A100 GPU

    // 定义操作类别（如Tensor Core或SIMT）
    using OpClass = cutlass::arch::OpClassSimt; // 使用标准CUDA核心简化示例

    // 定义线程块和warp分块尺寸（关键性能参数！）
    // ThreadblockShape: 线程块处理的总工作量（M, N, K）
    using ThreadblockShape = cutlass::gemm::GemmShape<128, 128, 8>;
    // WarpShape: 单个warp处理的工作量（M, N, K）
    using WarpShape = cutlass::gemm::GemmShape<32, 64, 8>; // 示例值
    // InstructionShape: 硬件指令的分块形状（如SIMT float使用1x1x1）
    using InstructionShape = cutlass::gemm::GemmShape<1, 1, 1>;

    // 定义尾声操作（如简单线性组合）
    using EpilogueOutputOp = cutlass::epilogue::thread::LinearCombination<
        ElementC, // 输出元素类型
        128 / sizeof(ElementC), // 每次访问加载/存储的元素数量
        ElementAccumulator, // 累加器元素类型
        ElementC // alpha/beta的计算元素类型
    >;

    // 定义实际GEMM内核类型
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
        cutlass::gemm::threadblock::GemmIdentityThreadblockSwizzle<>, // 线程块调度方式
        2 // 流水线阶段数
    >;

    // 2. 准备问题规模和数据
    long long M = 256;
    long long N = 256;
    long long K = 128;

    // 线性组合标量（C = alpha * A * B + beta * C）
    float alpha = 1.0f;
    float beta = 0.0f; // 对应C = A * B

    std::cout << "矩阵维度: M=" << M << ", N=" << N << ", K=" << K << std::endl;

    // 分配主机张量
    cutlass::HostTensor<ElementA, LayoutA> tensor_A({M, K});
    cutlass::HostTensor<ElementB, LayoutB> tensor_B({K, N});
    cutlass::HostTensor<ElementC, LayoutC> tensor_C({M, N});
    cutlass::HostTensor<ElementC, LayoutC> tensor_D_ref({M, N}); // CPU参考值

    // 用随机数据初始化主机张量
    cutlass::reference::host::TensorFillRandomUniform(tensor_A.host_data(), tensor_A.layout(), 0, 10);
    cutlass::reference::host::TensorFillRandomUniform(tensor_B.host_data(), tensor_B.layout(), 0, 10);
    cutlass::reference::host::TensorFillRandomUniform(tensor_C.host_data(), tensor_C.layout(), 0, 0); // 初始化C为零

    std::cout << "张量初始化完成" << std::endl;

    // 将主机张量复制到设备
    tensor_A.sync_device();
    tensor_B.sync_device();
    tensor_C.sync_device();

    std::cout << "数据已复制到GPU设备" << std::endl;

    // 3. 创建GEMM参数
    typename Gemm::Arguments arguments(
        {M, N, K},
        tensor_A.device_ref(),
        tensor_B.device_ref(),
        tensor_C.device_ref(),
        tensor_C.device_ref(), // 原地更新C
        {alpha, beta}
    );

    // 4. 创建并启动GEMM操作
    Gemm gemm_op;

    // 检查当前设备是否支持该内核
    cutlass::Status status = gemm_op.initialize(arguments);
    if (status != cutlass::Status::kSuccess) {
        std::cerr << "GEMM初始化失败: " << cutlass::cutlass_get_status_string(status) << std::endl;
        return 1; // 返回错误
    }

    std::cout << "GEMM内核初始化成功" << std::endl;

    // 启动内核
    status = gemm_op(arguments);
    if (status != cutlass::Status::kSuccess) {
        std::cerr << "GEMM启动失败: " << cutlass::cutlass_get_status_string(status) << std::endl;
        return 1; // 返回错误
    }

    std::cout << "GEMM内核执行完成" << std::endl;

    // 5. 将结果从设备复制回主机
    tensor_C.sync_host();

    // 6. 使用CPU参考值验证结果
    cutlass::reference::host::gemm(
        {M, N, K},
        alpha,
        tensor_A.host_ref(),
        tensor_B.host_ref(),
        beta,
        tensor_D_ref.host_ref(),
        tensor_D_ref.host_ref()
    );

    std::cout << "CPU参考计算完成" << std::endl;

    // 比较GPU和CPU结果
    bool passed = cutlass::reference::host::TensorEquals(
        tensor_C.host_ref(),
        tensor_D_ref.host_ref()
    );

    if (passed) {
        std::cout << "✓ GEMM测试通过！GPU和CPU结果一致。" << std::endl;
    } else {
        std::cout << "✗ GEMM测试失败！GPU和CPU结果不一致。" << std::endl;
        return 1;
    }

    // 打印一些结果统计信息
    std::cout << "\n结果统计:" << std::endl;
    std::cout << "矩阵A维度: " << M << "x" << K << std::endl;
    std::cout << "矩阵B维度: " << K << "x" << N << std::endl;
    std::cout << "矩阵C维度: " << M << "x" << N << std::endl;
    std::cout << "总计算量: " << (2 * M * N * K) << " 次浮点运算" << std::endl;

    return 0;
} 