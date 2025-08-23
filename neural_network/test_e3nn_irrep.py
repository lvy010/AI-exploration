#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
e3nn Irrep对象测试
测试不可约表示(Irreducible Representations)的创建和属性
"""

try:
    from e3nn.o3 import Irrep
    print("成功导入e3nn库\n")
except ImportError:
    print("错误: 无法导入e3nn库")
    print("请使用以下命令安装:")
    print("pip install e3nn")
    exit(1)

def test_basic_irreps():
    """测试基本的Irrep对象创建"""
    print("=== 基本Irrep对象测试 ===")
    
    # 标量(l=0, 偶宇称)
    scalar_irrep = Irrep("0e")
    print(f"标量Irrep: {scalar_irrep}, l={scalar_irrep.l}, p={scalar_irrep.p}, 维度={scalar_irrep.dim}")

    # 矢量(l=1, 奇宇称)
    vector_irrep = Irrep("1o")
    print(f"矢量Irrep: {vector_irrep}, l={vector_irrep.l}, p={vector_irrep.p}, 维度={vector_irrep.dim}")
    
    print()

def test_extended_irreps():
    """测试更多的Irrep对象"""
    print("=== 扩展Irrep对象测试 ===")
    
    # 测试更多的不可约表示
    irrep_specs = [
        "0e",  # 标量，偶宇称
        "0o",  # 伪标量，奇宇称
        "1e",  # 伪矢量，偶宇称
        "1o",  # 矢量，奇宇称
        "2e",  # 二阶张量，偶宇称
        "2o",  # 二阶伪张量，奇宇称
        "3e",  # 三阶张量，偶宇称
        "3o",  # 三阶伪张量，奇宇称
    ]
    
    for spec in irrep_specs:
        irrep = Irrep(spec)
        parity_name = "偶" if irrep.p == 1 else "奇"
        print(f"Irrep {spec}: l={irrep.l}, 宇称={parity_name}({irrep.p}), 维度={irrep.dim}")
    
    print()

def test_irrep_properties():
    """测试Irrep对象的属性和方法"""
    print("=== Irrep属性和方法测试 ===")
    
    # 创建一个l=2的Irrep
    irrep = Irrep("2e")
    
    print(f"Irrep: {irrep}")
    print(f"角动量量子数 l: {irrep.l}")
    print(f"宇称 p: {irrep.p}")
    print(f"维度: {irrep.dim}")
    print(f"字符串表示: {str(irrep)}")
    print(f"哈希值: {hash(irrep)}")
    
    # 测试相等性
    same_irrep = Irrep("2e")
    different_irrep = Irrep("2o")
    
    print(f"\n相等性测试:")
    print(f"Irrep('2e') == Irrep('2e'): {irrep == same_irrep}")
    print(f"Irrep('2e') == Irrep('2o'): {irrep == different_irrep}")
    
    print()

def test_irrep_multiplication():
    """测试Irrep的乘法运算（张量积）"""
    print("=== Irrep张量积测试 ===")
    
    # 创建两个Irrep
    irrep1 = Irrep("1o")  # 矢量
    irrep2 = Irrep("1o")  # 矢量
    
    print(f"Irrep1: {irrep1}")
    print(f"Irrep2: {irrep2}")
    
    # 计算张量积
    try:
        product = irrep1 * irrep2
        print(f"张量积 {irrep1} ⊗ {irrep2}:")
        for irrep, multiplicity in product:
            print(f"  {multiplicity} × {irrep}")
    except Exception as e:
        print(f"张量积计算出错: {e}")
    
    print()

def test_dimension_formula():
    """验证维度公式"""
    print("=== 维度公式验证 ===")
    
    print("球谐函数的维度公式: dim = 2l + 1")
    
    for l in range(6):
        irrep_e = Irrep(f"{l}e")
        irrep_o = Irrep(f"{l}o")
        expected_dim = 2 * l + 1
        
        print(f"l={l}: 期望维度={expected_dim}, "
              f"实际维度(偶)={irrep_e.dim}, "
              f"实际维度(奇)={irrep_o.dim}")
    
    print()

def demonstrate_physical_meaning():
    """演示不同Irrep的物理意义"""
    print("=== 物理意义演示 ===")
    
    physical_meanings = {
        "0e": "标量 (温度、密度、能量等)",
        "0o": "伪标量 (螺旋性等)",
        "1o": "极矢量 (位置、速度、电场等)",
        "1e": "轴矢量/伪矢量 (角动量、磁场等)",
        "2e": "对称张量 (应力张量、惯性张量等)",
        "2o": "反对称张量 (某些物理量)",
    }
    
    for spec, meaning in physical_meanings.items():
        irrep = Irrep(spec)
        print(f"{irrep}: {meaning}")
    
    print()

if __name__ == "__main__":
    print("E3NN Irrep对象测试程序")
    print("=" * 50)
    
    # 运行所有测试
    test_basic_irreps()
    test_extended_irreps()
    test_irrep_properties()
    test_irrep_multiplication()
    test_dimension_formula()
    demonstrate_physical_meaning()
    
    print("测试完成!")
