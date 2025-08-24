#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 e3nn.o3.Linear 模块的示例代码
演示如何创建等变线性层并验证其等变性
"""

import torch
from e3nn import o3

def test_basic_linear():
    """测试基本的线性层功能"""
    print("=" * 60)
    print("测试 e3nn.o3.Linear 基本功能")
    print("=" * 60)
    
    # 定义输入数据的Irreps：
    # 一个标量（0e）和一个向量（1o）的混合
    irreps_in = o3.Irreps("0e + 1o")
    print(f"输入Irreps: {irreps_in}")
    print(f"输入维度: {irreps_in.dim}")
    
    # 创建符合这些Irreps的随机输入数据
    x = irreps_in.randn(10, -1)  # 10个样本，其中-1被irreps_in.dim（4）替换
    print(f"输入数据形状: {x.shape}")
    print(f"输入数据示例（第一个样本）: {x[0]}")
    
    # 定义输出数据的Irreps：
    # 两个标量（0e）和两个向量（1o）的混合
    irreps_out = o3.Irreps("2x0e + 2x1o")
    print(f"输出Irreps: {irreps_out}")
    print(f"输出维度: {irreps_out.dim}")
    
    # 创建一个将'irreps_in'数据转换为'irreps_out'数据的线性层
    # e3nn确保此层尊重旋转/反射
    linear_layer = o3.Linear(irreps_in=irreps_in, irreps_out=irreps_out)
    print(f"\n线性层创建: {linear_layer}")
    print(f"权重数量: {sum(p.numel() for p in linear_layer.parameters())}")
    
    # 将线性层应用于输入数据
    y = linear_layer(x)
    print(f"输出数据形状: {y.shape}")
    print(f"输出数据示例（第一个样本）: {y[0]}")

def test_complex_linear():
    """测试更复杂的线性层配置"""
    print("\n" + "=" * 60)
    print("测试复杂线性层配置")
    print("=" * 60)
    
    # 更复杂的输入：包含多种不可约表示
    irreps_in = o3.Irreps("2x0e + 1x1o + 1x2e")
    print(f"输入Irreps: {irreps_in}")
    print(f"输入维度: {irreps_in.dim}")
    
    # 复杂的输出
    irreps_out = o3.Irreps("3x0e + 2x1o + 1x2e + 1x3o")
    print(f"输出Irreps: {irreps_out}")
    print(f"输出维度: {irreps_out.dim}")
    
    # 创建数据
    x = irreps_in.randn(5, -1)
    print(f"输入数据形状: {x.shape}")
    
    # 创建线性层
    complex_linear = o3.Linear(irreps_in=irreps_in, irreps_out=irreps_out)
    print(f"\n复杂线性层: {complex_linear}")
    print(f"权重数量: {sum(p.numel() for p in complex_linear.parameters())}")
    
    # 应用变换
    y = complex_linear(x)
    print(f"输出数据形状: {y.shape}")

def test_equivariance():
    """测试线性层的等变性"""
    print("\n" + "=" * 60)
    print("测试线性层的等变性")
    print("=" * 60)
    
    # 设置输入和输出Irreps
    irreps_in = o3.Irreps("1x0e + 1x1o")
    irreps_out = o3.Irreps("2x0e + 1x1o")
    
    print(f"输入Irreps: {irreps_in}")
    print(f"输出Irreps: {irreps_out}")
    
    # 创建输入数据
    x = irreps_in.randn(1, -1)
    print(f"原始输入: {x}")
    
    # 创建线性层
    linear = o3.Linear(irreps_in=irreps_in, irreps_out=irreps_out)
    
    # 创建随机旋转矩阵
    R = o3.rand_matrix()
    print(f"旋转矩阵:\n{R}")
    
    # 方法1：先旋转输入，再通过线性层
    D_in = irreps_in.D_from_matrix(R)  # 输入的旋转表示矩阵
    x_rotated = D_in @ x.T
    x_rotated = x_rotated.T
    y1 = linear(x_rotated)
    
    # 方法2：先通过线性层，再旋转输出
    y = linear(x)
    D_out = irreps_out.D_from_matrix(R)  # 输出的旋转表示矩阵
    y2_rotated = D_out @ y.T
    y2 = y2_rotated.T
    
    print(f"旋转后的输入: {x_rotated}")
    print(f"方法1 - 先旋转后线性变换: {y1}")
    print(f"方法2 - 先线性变换后旋转: {y2}")
    
    # 检查等变性
    is_equivariant = torch.allclose(y1, y2, atol=1e-6)
    print(f"等变性验证: {is_equivariant}")
    
    if not is_equivariant:
        diff = torch.abs(y1 - y2).max().item()
        print(f"最大差异: {diff}")
    else:
        print("✓ 线性层满足等变性！")

def test_weight_analysis():
    """分析线性层的权重结构"""
    print("\n" + "=" * 60)
    print("分析线性层权重结构")
    print("=" * 60)
    
    irreps_in = o3.Irreps("1x0e + 1x1o")
    irreps_out = o3.Irreps("2x0e + 1x1o")
    
    linear = o3.Linear(irreps_in=irreps_in, irreps_out=irreps_out)
    
    print(f"线性层: {linear}")
    print(f"权重参数:")
    
    total_params = 0
    for name, param in linear.named_parameters():
        print(f"  {name}: {param.shape} ({param.numel()} parameters)")
        total_params += param.numel()
    
    print(f"总参数数量: {total_params}")
    
    # 显示权重矩阵的连接模式
    print(f"\n权重矩阵形状分析:")
    print(f"输入维度: {irreps_in.dim}")
    print(f"输出维度: {irreps_out.dim}")
    print(f"如果是普通线性层，需要参数: {irreps_in.dim * irreps_out.dim}")
    print(f"等变线性层实际参数: {total_params}")
    print(f"参数效率: {total_params / (irreps_in.dim * irreps_out.dim):.2%}")

def test_different_parities():
    """测试不同宇称的组合"""
    print("\n" + "=" * 60)
    print("测试不同宇称的不可约表示")
    print("=" * 60)
    
    # 包含偶宇称和奇宇称的组合
    irreps_in = o3.Irreps("1x0e + 1x1o + 1x0o + 1x1e")
    irreps_out = o3.Irreps("2x0e + 1x1o + 1x2e")
    
    print(f"输入Irreps: {irreps_in}")
    print(f"输出Irreps: {irreps_out}")
    
    # 创建数据和线性层
    x = irreps_in.randn(3, -1)
    linear = o3.Linear(irreps_in=irreps_in, irreps_out=irreps_out)
    
    print(f"线性层: {linear}")
    
    # 应用变换
    y = linear(x)
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {y.shape}")
    
    # 验证宇称保持
    print(f"\n宇称分析:")
    print(f"输入包含: 偶标量(0e), 奇向量(1o), 奇标量(0o), 偶向量(1e)")
    print(f"输出包含: 偶标量(0e), 奇向量(1o), 偶2阶张量(2e)")
    print(f"宇称选择规则确保只有允许的连接存在")

if __name__ == "__main__":
    # 设置随机种子以获得可重现的结果
    torch.manual_seed(42)
    
    try:
        # 运行所有测试
        test_basic_linear()
        test_complex_linear()
        test_equivariance()
        test_weight_analysis()
        test_different_parities()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
