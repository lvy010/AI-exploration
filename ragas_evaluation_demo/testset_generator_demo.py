#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全流程整合：测试集生成器
TestsetGenerator是实现端到端测试集生成的核心入口
"""

import os
import asyncio
import pandas as pd
from datetime import datetime

def main():
    print("=" * 80)
    print("## 全流程整合：测试集生成器")
    print("TestsetGenerator是实现端到端测试集生成的核心入口")
    print("=" * 80)
    
    # 配置基础模型
    print("\n### 配置基础模型")
    print("```python")
    print("from ragas.llms import LangchainLLMWrapper")
    print("from langchain_openai import ChatOpenAI")
    print("")
    print("生成用LLM = LangchainLLMWrapper(ChatOpenAI(model=\"gpt-4o\"))")
    print("```")
    
    try:
        from ragas.llms import LangchainLLMWrapper
        from langchain_openai import ChatOpenAI
        
        # 确保已设置OPENAI_API_KEY环境变量
        生成用LLM = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
        print("✓ 基础模型配置完成")
        
    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        print("请先安装必要的依赖包: pip install ragas langchain-openai")
        return
    except Exception as e:
        print(f"✗ 配置错误: {e}")
        print("请确保已设置OPENAI_API_KEY环境变量")
        return
    
    # 准备示例文档
    print("\n### 准备示例文档")
    print("```python")
    print("from langchain_core.documents import Document as LCDocument")
    print("")
    print("文档集合 = [")
    print("    LCDocument(page_content=\"埃菲尔铁塔位于法国巴黎。\"),")
    print("    LCDocument(page_content=\"巴黎是法国的首都。\"),")
    print("    LCDocument(page_content=\"塞纳河流经巴黎。\"),")
    print("]")
    print("```")
    
    try:
        from langchain_core.documents import Document as LCDocument
        
        文档集合 = [
            LCDocument(page_content="埃菲尔铁塔位于法国巴黎。"),
            LCDocument(page_content="巴黎是法国的首都。"),
            LCDocument(page_content="塞纳河流经巴黎。"),
        ]
        print("✓ 示例文档准备完成")
        print(f"  - 文档数量: {len(文档集合)}")
        for i, doc in enumerate(文档集合, 1):
            print(f"  - 文档{i}: {doc.page_content}")
            
    except Exception as e:
        print(f"✗ 文档准备错误: {e}")
        return
    
    # 执行测试集生成
    print("\n### 执行测试集生成")
    print("```python")
    print("from ragas.testset.synthesizers import TestsetGenerator")
    print("")
    print("生成器 = TestsetGenerator(llm=生成用LLM)")
    print("生成测试集 = asyncio.run(")
    print("    生成器.generate_with_langchain_docs(文档集合, testset_size=3)")
    print(")")
    print("")
    print("# 结果展示")
    print("import pandas as pd")
    print("结果表 = 生成测试集.to_pandas()")
    print("print(结果表[['user_input', 'retrieved_contexts', 'reference']])")
    print("```")
    
    try:
        from ragas.testset.synthesizers import TestsetGenerator
        
        print("\n正在执行测试集生成...")
        生成器 = TestsetGenerator(llm=生成用LLM)
        
        # 使用asyncio运行异步生成
        生成测试集 = asyncio.run(
            生成器.generate_with_langchain_docs(文档集合, testset_size=3)
        )
        
        print("✓ 测试集生成完成")
        
        # 结果展示
        print("\n## 结果展示")
        结果表 = 生成测试集.to_pandas()
        
        # 显示关键列
        print("\n生成的测试集：")
        print(结果表[['user_input', 'retrieved_contexts', 'reference']].to_string(index=False))
        
        # 保存结果到CSV文件
        文件名 = f"测试集生成结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        结果表.to_csv(文件名, index=False, encoding='utf-8')
        print(f"\n✓ 测试集结果已保存到 '{文件名}'")
        
        # 显示完整结果
        print("\n完整测试集结果：")
        print(结果表.to_string(index=False))
        
    except Exception as e:
        print(f"✗ 测试集生成错误: {e}")
        print("\n创建模拟结果...")
        
        # 创建模拟结果
        模拟结果数据 = [
            {
                'user_input': '法国的首都是哪里？',
                'retrieved_contexts': ['巴黎是法国的首都。'],
                'reference': '巴黎'
            },
            {
                'user_input': '塞纳河流经哪个城市？',
                'retrieved_contexts': ['塞纳河流经巴黎。'],
                'reference': '巴黎'
            },
            {
                'user_input': '埃菲尔铁塔位于何处？',
                'retrieved_contexts': ['埃菲尔铁塔位于法国巴黎。'],
                'reference': '法国巴黎'
            }
        ]
        
        结果表 = pd.DataFrame(模拟结果数据)
        
        print("\n模拟生成的测试集：")
        print(结果表[['user_input', 'retrieved_contexts', 'reference']].to_string(index=False))
        
        # 保存模拟结果
        文件名 = f"测试集生成结果_模拟_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        结果表.to_csv(文件名, index=False, encoding='utf-8')
        print(f"\n✓ 模拟测试集结果已保存到 '{文件名}'")
    
    print("\n" + "=" * 80)
    print("## 输出示例：")
    print("```")
    print("                      user_input                       retrieved_contexts      reference")
    print("0          法国的首都是哪里？              [巴黎是法国的首都。]             巴黎")
    print("1        塞纳河流经哪个城市？            [塞纳河流经巴黎。]             巴黎")
    print("2        埃菲尔铁塔位于何处？      [埃菲尔铁塔位于法国巴黎。]           法国巴黎")
    print("```")
    print("=" * 80)
    
    print("\n## 测试集生成器功能特点：")
    print("✅ 自动从文档生成测试问题")
    print("✅ 智能匹配相关上下文")
    print("✅ 生成标准参考答案")
    print("✅ 支持批量处理")
    print("✅ 结果可导出为CSV格式")
    
    print("\n## 实际运行说明：")
    print("1. 设置OpenAI API密钥：export OPENAI_API_KEY='your-api-key-here'")
    print("2. 安装依赖：pip install ragas langchain-openai")
    print("3. 运行测试集生成：python3 testset_generator_demo.py")
    print("4. 查看生成的CSV文件获取详细结果")
    
    print("\n## 测试集生成完成！")
    print("TestsetGenerator端到端测试集生成演示成功完成。")

if __name__ == "__main__":
    main() 