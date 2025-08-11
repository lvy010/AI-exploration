# 智能体编排模式

## 概述

编排模式使智能体能够有效地执行工作流。编排模式通常分为两类：

1. **单智能体系统** - 单个模型配备适当的工具和指令
2. **多智能体系统** - 工作流执行分布在多个协调的智能体之间

## 单智能体系统

### 基本概念

单智能体可以通过逐步添加工具来处理许多任务，保持复杂性可管理。

### 运行循环

每个编排方法都需要"运行"的概念，通常实现为循环，让智能体运行直到达到退出条件。

```python
from agents import Agent, Runner, UserMessage

weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a helpful agent who can talk to users about the weather.",
    tools=[get_weather]
)

async def main():
    result = await Runner.run(weather_agent, [
        UserMessage("What's the weather like in Beijing?")
    ])
    print(result.final_output)
```

## 多智能体系统

### 管理器模式

管理器模式使中央LLM能够通过工具调用编排专业智能体网络。

```python
# 专业翻译智能体
spanish_agent = Agent(
    name="Spanish Translator",
    instructions="You translate text to Spanish accurately and naturally."
)

# 管理器智能体
manager_agent = Agent(
    name="Translation Manager",
    instructions="You are a translation agent. You use the tools given to you to translate.",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish"
        )
    ]
)
```

### 去中心化模式

智能体可以"转接"工作流执行给彼此。

```python
# 分流智能体
triage_agent = Agent(
    name="Triage Agent",
    instructions="You act as the first point of contact, assessing customer queries.",
    handoffs=[technical_support_agent, sales_assistant_agent]
)
```

## 实践

1. **渐进式开发**：从简单开始，逐步增加复杂性
2. **清晰的职责分离**：每个智能体有明确的职责
3. **错误处理**：包含错误检测和处理机制
