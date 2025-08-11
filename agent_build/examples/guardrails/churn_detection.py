#!/usr/bin/env python3
"""
客户流失检测安全护栏示例
演示如何使用安全护栏检测客户流失风险
"""

import asyncio
from dataclasses import dataclass

@dataclass
class GuardrailFunctionOutput:
    tripwire_triggered: bool
    output_info: str

@dataclass
class Guardrail:
    guardrail_function: callable
    name: str = ""

class Agent:
    def __init__(self, name: str, instructions: str, input_guardrails: list = None):
        self.name = name
        self.instructions = instructions
        self.input_guardrails = input_guardrails or []
    
    async def process_input(self, user_input: str) -> str:
        print(f"[{self.name}] 处理: {user_input}")
        
        # 检查安全护栏
        for guardrail in self.input_guardrails:
            try:
                result = await guardrail.guardrail_function(None, self, [user_input])
                if result.tripwire_triggered:
                    return f"安全护栏触发: {result.output_info}"
            except Exception as e:
                print(f"安全护栏错误: {e}")
        
        return "正常处理用户请求"

# 流失检测安全护栏
async def churn_detection_tripwire(ctx, agent, input_items):
    user_input = str(input_items[0]).lower()
    
    churn_keywords = ["取消", "退订", "不满意", "cancel", "unsubscribe"]
    is_risk = any(keyword in user_input for keyword in churn_keywords)
    
    return GuardrailFunctionOutput(
        tripwire_triggered=is_risk,
        output_info="检测到客户流失风险"
    )

def main():
    print("=== 客户流失检测安全护栏示例 ===\n")
    
    customer_agent = Agent(
        name="Customer Support Agent",
        instructions="You are a customer support agent.",
        input_guardrails=[
            Guardrail(churn_detection_tripwire, "流失检测")
        ]
    )
    
    test_cases = [
        "你好，我想了解一下产品",
        "我想取消订阅",
        "对服务不满意，想退订",
        "谢谢你的帮助"
    ]
    
    async def run_tests():
        for test_input in test_cases:
            print(f"\n用户输入: {test_input}")
            result = await customer_agent.process_input(test_input)
            print(f"结果: {result}")
    
    asyncio.run(run_tests())

if __name__ == "__main__":
    main() 