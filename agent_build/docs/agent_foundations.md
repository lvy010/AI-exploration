# 智能体设计基础

## 概述

智能体的最基本形式由三个核心组件组成：

1. **`模型` (Model)** - 为智能体的推理和决策提供动力的LLM
2. **`工具` (Tools)** - 智能体可以用来与外部系统交互的外部函数或API
3. **`指令` (Instructions)** - 定义智能体行为方式的明确指导原则和安全护栏

## 模型选择

### 不同模型的优势和权衡

不同的模型在任务复杂性、延迟和成本方面有不同的优势和权衡。在选择模型时，需要考虑：

- **任务复杂度**：简单任务可能只需要较小、较快的模型
- **延迟要求**：实时应用需要更快的响应时间
- **成本考虑**：更大模型通常成本更高

### 选择策略

1. **建立性能基线**：使用最强大的模型构建原型
2. **逐步优化**：尝试用较小的模型替换，看是否仍能达到可接受的结果
3. **评估指标**：关注准确性和性能目标

### 模型选择原则

```python
# 示例：根据任务复杂度选择模型
def select_model(task_complexity):
    if task_complexity == "simple":
        return "gpt-4o-mini"  # 快速、低成本
    elif task_complexity == "medium":
        return "gpt-4o"       # 平衡性能和成本
    else:
        return "gpt-4o-omni"  # 最高性能
```

## 工具定义

### 工具类型

智能体需要三种类型的工具：

#### 1. 数据工具 (Data Tools)

- **描述**：`使智能体能够检索执行工作流所需的上下文和信息`
- **示例**：查询交易数据库、读取PDF文档、搜索网络

#### 2. 行动工具 (Action Tools)

- **描述**：`使智能体能够与系统交互以执行操作`
- **示例**：发送电子邮件、更新CRM记录、转接客户服务工单

#### 3. 编排工具 (Orchestration Tools)

- **描述**：`智能体本身可以作为其他智能体的工具`
- **示例**：退款智能体、研究智能体、写作智能体

### 工具设计最佳实践

```python
from agents import Agent, function_tool

@function_tool
def get_weather(location: str) -> str:
    """获取指定位置的天气信息"""
    # 实现天气API调用
    return f"Weather in {location}: Sunny, 25°C"

@function_tool
def save_results(output: str) -> str:
    """保存结果到数据库"""
    # 实现数据库保存逻辑
    return "Results saved successfully"

# 创建智能体并装备工具
weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a helpful agent who can talk to users about the weather.",
    tools=[get_weather, save_results]
)
```

## 指令配置

### 高质量指令的重要性

清晰的指令对于任何LLM驱动的应用程序都至关重要，特别是对于智能体。良好的指令设计可以：

- 减少歧义
- 改善智能体决策
- 实现更流畅的工作流执行
- 减少错误

### 指令设计最佳实践

#### 1. 使用现有文档

```python
# 使用现有的操作程序创建LLM友好的例程
instructions = """
基于我们的客户服务知识库，按照以下步骤处理客户查询：
1. 确认客户身份
2. 理解问题类型
3. 应用相应的解决方案
4. 确认问题解决
"""
```

#### 2. 分解任务

```python
# 将复杂任务分解为更小、更清晰的步骤
instructions = """
处理退款请求的步骤：
1. 验证订单号
2. 检查退款资格
3. 计算退款金额
4. 执行退款操作
5. 发送确认邮件
"""
```

#### 3. 定义明确的操作

```python
# 确保每个步骤对应特定的操作或输出
instructions = """
当用户提供订单号时：
- 调用 get_order_details(order_number) 函数
- 如果订单不存在，回复："抱歉，找不到该订单"
- 如果订单存在，显示订单详情
"""
```

#### 4. 处理边缘情况

```python
# 预期常见变化并包含处理指令
instructions = """
如果用户提供的信息不完整：
- 询问缺失的信息
- 提供示例格式
- 最多询问3次，然后转接人工客服
"""
```

### 自动生成指令

可以使用高级模型（如o1或o3-mini）从现有文档自动生成指令：

```python
instruction_prompt = """
You are an expert in writing instructions for an LLM agent. 
Convert the following help center document into a clear set of instructions, 
written in a numbered list. The document will be a policy followed by an LLM. 
Ensure that there is no ambiguity, and that the instructions are written as 
directions for an agent. The help center document to convert is the following: 
{{help_center_doc}}
"""
```

## 代码示例

### 基础智能体创建

```python
from agents import Agent, Runner

# 创建基础智能体
basic_agent = Agent(
    name="Basic Agent",
    instructions="You are a helpful assistant that can answer questions.",
    tools=[]  # 没有工具的基础智能体
)

# 运行智能体
async def main():
    result = await Runner.run(basic_agent, "What is the capital of France?")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### 带工具的智能体

```python
from agents import Agent, Runner, function_tool
from datetime import datetime

@function_tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

# 创建多功能智能体
utility_agent = Agent(
    name="Utility Agent",
    instructions="""
    你是一个实用工具智能体，可以帮助用户：
    1. 获取当前时间
    2. 进行数学计算
    3. 回答一般性问题
  
    当用户需要时间信息时，使用get_current_time工具
    当用户需要计算时，使用calculate工具
    """,
    tools=[get_current_time, calculate]
)
```

## 总结

智能体设计基础包括：

1. **`选择合适的模型`**：根据任务复杂度和性能要求
2. **`定义有用的工具`**：数据、行动和编排工具
3. **`编写清晰的指令`**：减少歧义，提高性能
4. **`迭代优化`**：从简单开始，逐步增加复杂性

记住，好的智能体设计是一个迭代过程。从简单的基础开始，然后根据实际使用情况逐步改进和扩展。
