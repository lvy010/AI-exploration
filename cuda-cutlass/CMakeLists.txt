cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

project(cutlass_gemm_example CUDA CXX)

# 设置C++标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 查找CUDA
find_package(CUDA REQUIRED)

# 设置CUDA架构（根据你的GPU调整）
set(CMAKE_CUDA_ARCHITECTURES 80)  # 适用于A100 GPU，如果是其他GPU请调整

# 包含CUTLASS头文件路径
# 首先尝试使用本地克隆的CUTLASS
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/cutlass/include/cutlass/cutlass.h")
    set(CUTLASS_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/cutlass")
    include_directories(${CUTLASS_ROOT}/include)
    message(STATUS "找到本地CUTLASS在: ${CUTLASS_ROOT}")
elseif(DEFINED ENV{CUTLASS_ROOT})
    set(CUTLASS_ROOT $ENV{CUTLASS_ROOT})
    include_directories(${CUTLASS_ROOT}/include)
    message(STATUS "找到环境变量CUTLASS在: ${CUTLASS_ROOT}")
elseif(EXISTS "/usr/local/cutlass/include/cutlass/cutlass.h")
    set(CUTLASS_ROOT "/usr/local/cutlass")
    include_directories(${CUTLASS_ROOT}/include)
    message(STATUS "找到系统CUTLASS在: ${CUTLASS_ROOT}")
else()
    message(FATAL_ERROR "未找到CUTLASS。请确保CUTLASS已正确安装或克隆到本地。")
endif()

# 创建可执行文件
add_executable(gemm_example gemm_example.cpp)

# 设置CUDA编译选项
set_target_properties(gemm_example PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    CUDA_ARCHITECTURES ${CMAKE_CUDA_ARCHITECTURES}
)

# 链接CUDA库
target_link_libraries(gemm_example
    ${CUDA_LIBRARIES}
    cudart
    cublas
)

# 设置编译选项
target_compile_options(gemm_example PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:-Xcompiler=-Wall>
    $<$<COMPILE_LANGUAGE:CXX>:-Wall>
)

# 如果使用CUTLASS的静态库，取消注释下面的行
# target_link_libraries(gemm_example cutlass) 