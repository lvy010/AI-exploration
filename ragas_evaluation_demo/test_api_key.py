#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAI API密钥测试程序
用于验证API密钥是否正确设置
"""

import os

def test_api_key():
    """测试OpenAI API密钥是否设置正确"""
    print("=" * 50)
    print("OpenAI API密钥测试程序")
    print("=" * 50)
    
    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("✗ OpenAI API密钥未设置")
        print("\n请按照以下步骤设置API密钥：")
        print("1. 访问 https://platform.openai.com/api-keys")
        print("2. 登录并创建新的API密钥")
        print("3. 设置环境变量：")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\n或者临时设置（当前会话）：")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    print("✓ OpenAI API密钥已设置")
    print(f"密钥前10位: {api_key[:10]}...")
    
    # 测试API连接
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✓ API连接测试成功")
        print(f"响应内容: {response.choices[0].message.content}")
        return True
        
    except ImportError:
        print("✗ 缺少openai库，请安装：pip install openai")
        return False
    except Exception as e:
        print(f"✗ API连接测试失败: {e}")
        print("\n可能的原因：")
        print("1. API密钥无效或已过期")
        print("2. 网络连接问题")
        print("3. OpenAI服务暂时不可用")
        return False

if __name__ == "__main__":
    success = test_api_key()
    
    if success:
        print("\n" + "=" * 50)
        print("✓ API密钥设置成功！")
        print("现在可以运行RAGAS评估测试了：")
        print("python3 ragas_demo.py")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("✗ 请先解决API密钥问题")
        print("详细设置指南请查看：setup_api_key.md")
        print("=" * 50) 