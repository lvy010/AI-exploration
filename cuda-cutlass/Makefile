# CUTLASS GEMM示例 Makefile

# 编译器设置
NVCC = nvcc
CXX = g++

# CUDA路径（根据你的系统调整）
CUDA_PATH ?= /usr/local/cuda
CUTLASS_ROOT ?= $(shell if [ -d "cutlass" ]; then echo "$(PWD)/cutlass"; else echo "/usr/local/cutlass"; fi)

# 编译选项
NVCC_FLAGS = -std=c++17 -O3 -arch=sm_80
CXX_FLAGS = -std=c++17 -O3 -Wall

# 包含路径
INCLUDES = -I$(CUDA_PATH)/include -I$(CUTLASS_ROOT)/include -I$(CUTLASS_ROOT)/tools/util/include

# 库路径和库
LIBRARIES = -L$(CUDA_PATH)/lib64 -lcudart -lcublas

# 目标文件
TARGET = gemm_example
SIMPLE_TARGET = simple_gemm_example
CPU_TARGET = cpu_gemm_example
SOURCE = gemm_example.cpp
SIMPLE_SOURCE = simple_gemm_example.cpp
CPU_SOURCE = cpu_gemm_example.cpp

# 默认目标
all: $(TARGET) $(SIMPLE_TARGET) $(CPU_TARGET)

# 编译CUTLASS GEMM示例
$(TARGET): $(SOURCE)
	$(NVCC) $(NVCC_FLAGS) $(INCLUDES) -o $@ $< $(LIBRARIES)

# 编译简单GEMM示例
$(SIMPLE_TARGET): $(SIMPLE_SOURCE)
	$(NVCC) $(NVCC_FLAGS) $(INCLUDES) -o $@ $< $(LIBRARIES)

# 编译CPU GEMM示例
$(CPU_TARGET): $(CPU_SOURCE)
	$(CXX) $(CXX_FLAGS) -o $@ $<

# 清理
clean:
	rm -f $(TARGET) $(SIMPLE_TARGET) $(CPU_TARGET)

# 运行CUTLASS测试
test: $(TARGET)
	./$(TARGET)

# 运行简单测试
test-simple: $(SIMPLE_TARGET)
	./$(SIMPLE_TARGET)

# 运行CPU测试
test-cpu: $(CPU_TARGET)
	./$(CPU_TARGET)

# 检查CUDA和CUTLASS环境
check-env:
	@echo "检查CUDA环境..."
	@if [ -d "$(CUDA_PATH)" ]; then \
		echo "✓ CUDA路径存在: $(CUDA_PATH)"; \
	else \
		echo "✗ CUDA路径不存在: $(CUDA_PATH)"; \
		echo "请设置CUDA_PATH环境变量"; \
	fi
	@echo "检查CUTLASS环境..."
	@if [ -d "$(CUTLASS_ROOT)" ]; then \
		echo "✓ CUTLASS路径存在: $(CUTLASS_ROOT)"; \
	else \
		echo "✗ CUTLASS路径不存在: $(CUTLASS_ROOT)"; \
		echo "请设置CUTLASS_ROOT环境变量或安装CUTLASS"; \
	fi

# 帮助信息
help:
	@echo "可用的目标:"
	@echo "  all         - 构建所有GEMM示例"
	@echo "  $(TARGET)   - 构建CUTLASS GEMM示例"
	@echo "  $(SIMPLE_TARGET) - 构建简单GEMM示例"
	@echo "  $(CPU_TARGET) - 构建CPU GEMM示例"
	@echo "  clean       - 清理构建文件"
	@echo "  test        - 运行CUTLASS GEMM测试"
	@echo "  test-simple - 运行简单GEMM测试"
	@echo "  test-cpu    - 运行CPU GEMM测试"
	@echo "  check-env   - 检查CUDA和CUTLASS环境"
	@echo "  help        - 显示此帮助信息"

.PHONY: all clean test test-simple test-cpu check-env help 