#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有 e3nn 测试的主脚本
"""

import sys
import subprocess
import os

def run_test_file(filename):
    """运行单个测试文件"""
    print(f"\n{'='*80}")
    print(f"运行测试文件: {filename}")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run([sys.executable, filename], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(f"✓ {filename} 测试成功完成")
            print(result.stdout)
        else:
            print(f"✗ {filename} 测试失败")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            
    except Exception as e:
        print(f"✗ 运行 {filename} 时出错: {e}")

def main():
    """主函数"""
    print("开始运行所有 e3nn 测试...")
    
    # 测试文件列表
    test_files = [
        "test_e3nn_irrep.py",
        "test_e3nn_gate.py", 
        "test_e3nn_linear.py"
    ]
    
    # 检查文件是否存在
    missing_files = []
    for test_file in test_files:
        if not os.path.exists(test_file):
            missing_files.append(test_file)
    
    if missing_files:
        print(f"缺少测试文件: {missing_files}")
        return
    
    # 运行所有测试
    for test_file in test_files:
        run_test_file(test_file)
    
    print(f"\n{'='*80}")
    print("所有测试运行完成！")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
