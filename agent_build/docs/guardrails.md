# 智能体安全护栏

## 概述

安全护栏帮助管理数据隐私风险和声誉风险，是LLM部署的关键组件。

## 安全护栏类型

### 1. 相关性分类器
确保智能体响应保持在预期范围内。

### 2. 安全分类器
检测不安全的输入（越狱或提示注入）。

### 3. PII过滤器
防止个人身份信息的不必要暴露。

### 4. 工具安全措施
评估工具风险，基于访问类型和影响。

## 代码示例

```python
from agents import Agent, Guardrail, input_guardrail
from pydantic import BaseModel

class ChurnDetectionOutput(BaseModel):
    is_churn_risk: bool
    reasoning: str

@input_guardrail
async def churn_detection_tripwire(ctx, agent, input_items):
    # 检测客户流失风险
    user_input = str(input_items[0].content)
    is_risk = "cancel" in user_input.lower() or "unsubscribe" in user_input.lower()
    
    return GuardrailFunctionOutput(
        tripwire_triggered=is_risk,
        output_info="Potential churn risk detected"
    )

customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent.",
    input_guardrails=[
        Guardrail(guardrail_function=churn_detection_tripwire)
    ]
)
```

## 实践

1. **分层防御**：使用多个专业安全护栏
2. **持续监控**：监控安全护栏触发情况
3. **人工干预**：为高风险操作设置人工监督
4. **定期更新**：根据新威胁更新安全护栏 