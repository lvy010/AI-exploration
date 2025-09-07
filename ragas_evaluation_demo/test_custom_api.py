#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义API Host测试程序
支持配置自定义的OpenAI API端点
"""

import os

def test_custom_api():
    """测试自定义API host"""
    print("=" * 70)
    print("自定义API Host测试程序")
    print("=" * 70)
    
    # 获取API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ 未找到OPENAI_API_KEY环境变量")
        print("请设置：export OPENAI_API_KEY='sk-IdjVdqc65k03LgYWnLDWn3eMsBXOQON5weMjDAdE3FtJqUs3'")
        return False
    
    print("✓ API密钥已设置")
    print(f"密钥前10位: {api_key[:10]}...")
    
    # 自定义API host
    custom_host = "https://api.chatanywhere.tech/"
    print(f"自定义API Host: {custom_host}")
    
    try:
        from openai import OpenAI
        
        # 创建客户端，使用自定义host
        client = OpenAI(
            api_key=api_key,
            base_url=custom_host
        )
        
        print("\n🔍 测试API连接...")
        
        # 测试连接
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print("✓ API连接测试成功！")
        print(f"响应内容: {response.choices[0].message.content}")
        return True
        
    except ImportError:
        print("✗ 缺少openai库，请安装：pip install openai")
        return False
    except Exception as e:
        error_msg = str(e)
        print(f"✗ API连接测试失败: {error_msg}")
        
        # 分析错误类型
        if "invalid_api_key" in error_msg or "401" in error_msg:
            print("\n🔍 错误分析：API密钥无效")
            print("解决方案：检查密钥是否正确")
        elif "insufficient_quota" in error_msg or "429" in error_msg:
            print("\n🔍 错误分析：API配额已用完")
            print("解决方案：检查账户余额")
        elif "rate_limit" in error_msg:
            print("\n🔍 错误分析：请求频率过高")
            print("解决方案：等待一段时间后重试")
        else:
            print("\n🔍 错误分析：其他问题")
            print("可能的原因：")
            print("1. 网络连接问题")
            print("2. API host不可用")
            print("3. 防火墙或代理设置")
        
        return False

def test_ragas_with_custom_api():
    """测试RAGAS与自定义API的集成"""
    print("\n" + "=" * 70)
    print("RAGAS自定义API集成测试")
    print("=" * 70)
    
    try:
        from ragas.llms import LangchainLLMWrapper
        from langchain_openai import ChatOpenAI
        
        print("✓ RAGAS和LangChain导入成功")
        
        # 配置自定义API的LLM
        custom_host = "https://api.chatanywhere.tech/"
        api_key = os.getenv("OPENAI_API_KEY")
        
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=api_key,
            openai_api_base=custom_host
        )
        
        # 包装为RAGAS LLM
        ragas_llm = LangchainLLMWrapper(llm)
        print("✓ RAGAS LLM配置成功（使用自定义API）")
        
        return True
        
    except ImportError as e:
        print(f"✗ RAGAS导入失败: {e}")
        print("请安装RAGAS：pip install ragas")
        return False
    except Exception as e:
        print(f"✗ RAGAS配置失败: {e}")
        return False

if __name__ == "__main__":
    # 测试自定义API
    api_success = test_custom_api()
    
    # 测试RAGAS集成
    ragas_success = test_ragas_with_custom_api()
    
    print("\n" + "=" * 70)
    if api_success and ragas_success:
        print("🎉 所有测试通过！")
        print("现在可以运行RAGAS评估测试了：")
        print("python3 ragas_demo_custom.py")
        print("python3 testset_generator_demo_custom.py")
    elif api_success:
        print("⚠️  API测试通过，但RAGAS集成有问题")
        print("请检查RAGAS安装：pip install ragas")
    else:
        print("❌ 请先解决API问题")
    print("=" * 70) 