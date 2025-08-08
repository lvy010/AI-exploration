#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAGAS评估协调器实战应用
通过三步即可完成端到端评估
"""

import os
import pandas as pd

# 步骤1：配置基础模型
print("## 步骤1：配置基础模型")
print("正在配置评估用LLM与Embeddings...")

try:
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    
    # 确保已设置OPENAI_API_KEY环境变量
    评估用LLM = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
    评估用Embeddings = LangchainEmbeddingsWrapper(
        OpenAIEmbeddings(model="text-embedding-ada-002")
    )
    print("✓ 基础模型配置完成")
except ImportError as e:
    print(f"✗ 导入错误: {e}")
    print("请先安装必要的依赖包: pip install ragas langchain-openai")
    exit(1)
except Exception as e:
    print(f"✗ 配置错误: {e}")
    print("请确保已设置OPENAI_API_KEY环境变量")
    exit(1)

# 步骤2：准备数据集与指标
print("\n## 步骤2：准备数据集与指标")
print("正在构建微型数据集...")

try:
    from ragas import SingleTurnSample, EvaluationDataset
    
    样本1 = SingleTurnSample(
        user_input="法国的首都是哪里？",
        retrieved_contexts=["巴黎是法国的首都。"],
        response="法国的首都是巴黎。",
        reference="巴黎"
    )
    
    样本2 = SingleTurnSample(
        user_input="泰坦尼克号何时沉没？",
        retrieved_contexts=["泰坦尼克号于1912年4月15日沉没。"],
        response="泰坦尼克号于1912年4月15日沉没。",
        reference="1912年4月15日"
    )
    
    数据集实例 = EvaluationDataset(samples=[样本1, 样本2])
    print("✓ 数据集构建完成")
    
    # 初始化评估指标
    print("正在初始化评估指标...")
    from ragas.metrics import faithfulness, answer_relevancy
    
    faithfulness.llm = 评估用LLM
    answer_relevancy.llm = 评估用LLM
    answer_relevancy.embeddings = 评估用Embeddings
    print("✓ 评估指标初始化完成")
    
except Exception as e:
    print(f"✗ 数据集准备错误: {e}")
    exit(1)

# 步骤3：执行全量评估
print("\n## 步骤3：执行全量评估")
print("正在执行评估...")

try:
    from ragas import evaluate
    
    评估结果 = evaluate(
        dataset=数据集实例,
        metrics=[faithfulness, answer_relevancy]
    )
    
    print("✓ 评估执行完成")
    print("\n## 综合评估结果：")
    print(评估结果)  # 示例输出：{'faithfulness': 0.98, 'answer_relevancy': 0.95}
    
except Exception as e:
    print(f"✗ 评估执行错误: {e}")
    exit(1)

# 详细结果分析
print("\n## 详细结果分析")
try:
    详细结果表 = 评估结果.to_pandas()
    print("\n样本级评估明细：")
    print(详细结果表)
    
    # 保存结果到CSV文件
    详细结果表.to_csv('评估结果明细.csv', index=False, encoding='utf-8')
    print("\n✓ 详细结果已保存到 '评估结果明细.csv'")
    
except Exception as e:
    print(f"✗ 结果分析错误: {e}")

print("\n## 评估完成！")
print("RAGAS评估协调器实战应用演示成功完成。") 