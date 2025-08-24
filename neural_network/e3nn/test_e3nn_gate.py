#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 e3nn.nn.Gate 模块的示例代码
演示如何使用门控机制处理不同类型的不可约表示
"""

import torch
from e3nn import o3
from e3nn.nn import Gate

def test_gate_module():
    """测试 Gate 模块的基本功能"""
    print("=" * 60)
    print("测试 e3nn.nn.Gate 模块")
    print("=" * 60)
    
    # 示例：假设输入特征是两个标量和一个向量
    # 输入将是：1x0e（标量特征）+ 1x0e（门标量）+ 1x1o（向量特征）
    irreps_in = o3.Irreps("1x0e + 1x0e + 1x1o")
    x = irreps_in.randn(1, -1)
    print(f"输入Irreps: {irreps_in}")
    print(f"输入数据形状: {x.shape}")
    print(f"输入数据: {x}")
    
    # 定义Gate模块：
    # - 第一个0e将直接激活（无门控）。
    # - 第二个0e将被激活并用作门。
    # - 1o将由激活的第二个0e门控。
    equivariant_gate = Gate(
        irreps_scalars="1x0e",       # 一个0e标量
        act_scalars=[torch.tanh],    # 对其应用tanh
        irreps_gates="1x0e",         # 一个0e标量作为门
        act_gates=[torch.sigmoid],   # 对门标量应用sigmoid
        irreps_gated="1x1o"          # 一个1o向量被门控
    )
    print(f"\n等变Gate创建: {equivariant_gate}")
    print(f"输出Irreps: {equivariant_gate.irreps_out}")
    
    # 将Gate应用于输入数据
    y = equivariant_gate(x)
    print(f"输出数据形状: {y.shape}")
    print(f"输出数据: {y}")
    
    # 让我们手动拆分输入以检查输出（详细说明）
    print(f"\n详细分析:")
    print(f"输入irreps的切片信息: {irreps_in.slices()}")
    
    # 手动提取各部分
    scalars_input = x[:, irreps_in.slices()[0]]  # 第一个0e
    gates_input = x[:, irreps_in.slices()[1]]    # 第二个0e（门）
    gated_input = x[:, irreps_in.slices()[2]]    # 1o向量
    
    print(f"标量输入: {scalars_input}")
    print(f"门输入: {gates_input}")
    print(f"被门控的向量输入: {gated_input}")
    
    # 手动计算期望输出
    activated_scalars = torch.tanh(scalars_input)
    activated_gates = torch.sigmoid(gates_input)
    gated_vectors = activated_gates * gated_input
    
    print(f"\n手动计算结果:")
    print(f"激活标量 (tanh): {activated_scalars}")
    print(f"激活门 (sigmoid): {activated_gates}")
    print(f"门控向量: {gated_vectors}")
    
    # 验证结果
    expected_output = torch.cat([activated_scalars, gated_vectors], dim=1)
    print(f"期望输出: {expected_output}")
    print(f"实际输出: {y}")
    print(f"输出匹配: {torch.allclose(y, expected_output, atol=1e-6)}")

def test_complex_gate():
    """测试更复杂的门控配置"""
    print("\n" + "=" * 60)
    print("测试复杂门控配置")
    print("=" * 60)
    
    # 更复杂的输入：多个标量、多个门、多个向量
    irreps_in = o3.Irreps("2x0e + 2x0e + 1x1o + 1x2e")
    x = irreps_in.randn(1, -1)
    print(f"输入Irreps: {irreps_in}")
    print(f"输入数据形状: {x.shape}")
    
    # 定义更复杂的Gate
    complex_gate = Gate(
        irreps_scalars="2x0e",                    # 两个标量直接激活
        act_scalars=[torch.tanh, torch.relu],    # 不同的激活函数
        irreps_gates="2x0e",                      # 两个门标量
        act_gates=[torch.sigmoid, torch.sigmoid], # 门的激活函数
        irreps_gated="1x1o + 1x2e"               # 一个向量和一个2阶张量被门控
    )
    
    print(f"复杂Gate: {complex_gate}")
    print(f"输出Irreps: {complex_gate.irreps_out}")
    
    # 应用门控
    y = complex_gate(x)
    print(f"输出数据形状: {y.shape}")
    print(f"输出数据: {y}")

def test_gate_equivariance():
    """测试门控的等变性"""
    print("\n" + "=" * 60)
    print("测试门控的等变性")
    print("=" * 60)
    
    # 创建输入和旋转
    irreps_in = o3.Irreps("1x0e + 1x0e + 1x1o")
    x = irreps_in.randn(1, -1)
    
    # 创建随机旋转
    R = o3.rand_matrix()
    print(f"旋转矩阵:\n{R}")
    
    # 创建门控模块
    gate = Gate(
        irreps_scalars="1x0e",
        act_scalars=[torch.tanh],
        irreps_gates="1x0e",
        act_gates=[torch.sigmoid],
        irreps_gated="1x1o"
    )
    
    # 方法1：先旋转后门控
    x_rotated = irreps_in.D_from_matrix(R) @ x.T
    x_rotated = x_rotated.T
    y1 = gate(x_rotated)
    
    # 方法2：先门控后旋转
    y = gate(x)
    y2_rotated = gate.irreps_out.D_from_matrix(R) @ y.T
    y2 = y2_rotated.T
    
    print(f"原始输入: {x}")
    print(f"旋转后输入: {x_rotated}")
    print(f"方法1 - 先旋转后门控: {y1}")
    print(f"方法2 - 先门控后旋转: {y2}")
    print(f"等变性验证 (应该相等): {torch.allclose(y1, y2, atol=1e-6)}")
    
    # 显示差异
    if not torch.allclose(y1, y2, atol=1e-6):
        print(f"差异: {torch.abs(y1 - y2).max().item()}")

if __name__ == "__main__":
    # 设置随机种子以获得可重现的结果
    torch.manual_seed(42)
    
    try:
        # 运行所有测试
        test_gate_module()
        test_complex_gate()
        test_gate_equivariance()
        
        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
