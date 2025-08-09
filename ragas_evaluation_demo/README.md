# RAGAS评估协调器实战应用

这是一个完整的RAGAS（Retrieval-Augmented Generation Assessment）评估协调器实战应用演示。

## 功能特点

- **三步完成端到端评估**：配置模型 → 准备数据 → 执行评估
- **中文支持**：完全中文化的代码和输出
- **错误处理**：完善的异常处理和用户友好的错误提示
- **结果导出**：自动保存评估结果到CSV文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

确保设置OpenAI API密钥：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 运行演示

```bash
python ragas_demo.py
```

## 预期输出

程序将按以下步骤执行：

1. **配置基础模型** - 设置评估用LLM和Embeddings
2. **准备数据集与指标** - 构建测试数据集和评估指标
3. **执行全量评估** - 运行faithfulness和answer_relevancy评估
4. **详细结果分析** - 显示样本级评估明细并保存到CSV

## 文件说明

- `ragas_demo.py` - 主演示程序
- `requirements.txt` - 项目依赖
- `README.md` - 项目说明
- `评估结果明细.csv` - 运行后生成的评估结果文件

## 注意事项

- 需要有效的OpenAI API密钥
- 确保网络连接正常以访问OpenAI服务
- 首次运行可能需要下载模型，请耐心等待 