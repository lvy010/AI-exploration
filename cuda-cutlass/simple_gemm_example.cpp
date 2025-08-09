#include <iostream>
#include <vector>
#include <cuda_runtime.h>
#include <cublas_v2.h>

// 简单的GEMM实现，用于演示CUTLASS的概念
class SimpleGEMM {
private:
    cublasHandle_t handle_;
    
public:
    SimpleGEMM() {
        cublasCreate(&handle_);
    }
    
    ~SimpleGEMM() {
        cublasDestroy(handle_);
    }
    
    // 执行GEMM操作: C = alpha * A * B + beta * C
    bool execute(int M, int N, int K, 
                 float alpha, float beta,
                 const float* A, const float* B, float* C) {
        
        // 使用cuBLAS进行GEMM计算
        cublasStatus_t status = cublasSgemm(handle_,
                                           CUBLAS_OP_N,  // A不转置
                                           CUBLAS_OP_N,  // B不转置
                                           M, N, K,      // 矩阵维度
                                           &alpha,       // alpha标量
                                           A, M,         // A矩阵，列优先
                                           B, K,         // B矩阵，列优先
                                           &beta,        // beta标量
                                           C, M);        // C矩阵，列优先
        
        return (status == CUBLAS_STATUS_SUCCESS);
    }
};

// 验证函数：在CPU上计算参考结果
void cpu_gemm(int M, int N, int K, 
              float alpha, float beta,
              const std::vector<float>& A, 
              const std::vector<float>& B, 
              std::vector<float>& C) {
    
    // 简单的CPU GEMM实现
    for (int i = 0; i < M; ++i) {
        for (int j = 0; j < N; ++j) {
            float sum = 0.0f;
            for (int k = 0; k < K; ++k) {
                sum += A[i + k * M] * B[k + j * K];
            }
            C[i + j * M] = alpha * sum + beta * C[i + j * M];
        }
    }
}

int main() {
    std::cout << "简单GEMM示例开始..." << std::endl;
    
    // 矩阵维度
    int M = 256;
    int N = 256;
    int K = 128;
    
    std::cout << "矩阵维度: M=" << M << ", N=" << N << ", K=" << K << std::endl;
    
    // 分配主机内存
    std::vector<float> h_A(M * K);
    std::vector<float> h_B(K * N);
    std::vector<float> h_C(M * N);
    std::vector<float> h_C_ref(M * N);
    
    // 初始化矩阵
    for (int i = 0; i < M * K; ++i) {
        h_A[i] = static_cast<float>(rand()) / RAND_MAX;
    }
    for (int i = 0; i < K * N; ++i) {
        h_B[i] = static_cast<float>(rand()) / RAND_MAX;
    }
    for (int i = 0; i < M * N; ++i) {
        h_C[i] = 0.0f;
        h_C_ref[i] = 0.0f;
    }
    
    std::cout << "矩阵初始化完成" << std::endl;
    
    // 分配设备内存
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, M * K * sizeof(float));
    cudaMalloc(&d_B, K * N * sizeof(float));
    cudaMalloc(&d_C, M * N * sizeof(float));
    
    // 复制数据到设备
    cudaMemcpy(d_A, h_A.data(), M * K * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B.data(), K * N * sizeof(float), cudaMemcpyHostToDevice);
    cudaMemcpy(d_C, h_C.data(), M * N * sizeof(float), cudaMemcpyHostToDevice);
    
    std::cout << "数据已复制到GPU设备" << std::endl;
    
    // 执行GEMM
    SimpleGEMM gemm;
    float alpha = 1.0f;
    float beta = 0.0f;
    
    bool success = gemm.execute(M, N, K, alpha, beta, d_A, d_B, d_C);
    
    if (!success) {
        std::cerr << "GEMM执行失败！" << std::endl;
        return 1;
    }
    
    std::cout << "GEMM执行完成" << std::endl;
    
    // 复制结果回主机
    cudaMemcpy(h_C.data(), d_C, M * N * sizeof(float), cudaMemcpyDeviceToHost);
    
    // 在CPU上计算参考结果
    cpu_gemm(M, N, K, alpha, beta, h_A, h_B, h_C_ref);
    
    std::cout << "CPU参考计算完成" << std::endl;
    
    // 比较结果
    bool passed = true;
    float tolerance = 1e-5f;
    for (int i = 0; i < M * N; ++i) {
        if (std::abs(h_C[i] - h_C_ref[i]) > tolerance) {
            passed = false;
            break;
        }
    }
    
    if (passed) {
        std::cout << "✓ GEMM测试通过！GPU和CPU结果一致。" << std::endl;
    } else {
        std::cout << "✗ GEMM测试失败！GPU和CPU结果不一致。" << std::endl;
        return 1;
    }
    
    // 打印统计信息
    std::cout << "\n结果统计:" << std::endl;
    std::cout << "矩阵A维度: " << M << "x" << K << std::endl;
    std::cout << "矩阵B维度: " << K << "x" << N << std::endl;
    std::cout << "矩阵C维度: " << M << "x" << N << std::endl;
    std::cout << "总计算量: " << (2 * M * N * K) << " 次浮点运算" << std::endl;
    
    // 清理设备内存
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    
    return 0;
} 