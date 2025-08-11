#!/usr/bin/env python3
"""
天气智能体示例
演示单智能体系统的基本用法
"""

import asyncio
import os
from datetime import datetime
from typing import Optional

# 模拟天气API
class WeatherAPI:
    """模拟天气API服务"""
    
    def __init__(self):
        self.weather_data = {
            "北京": {"temperature": 25, "condition": "晴天", "humidity": 60},
            "上海": {"temperature": 28, "condition": "多云", "humidity": 70},
            "广州": {"temperature": 30, "condition": "雨天", "humidity": 80},
            "深圳": {"temperature": 29, "condition": "晴天", "humidity": 65},
        }
    
    def get_weather(self, city: str) -> Optional[dict]:
        """获取指定城市的天气信息"""
        return self.weather_data.get(city, None)

# 模拟智能体框架
class Agent:
    """简化的智能体类"""
    
    def __init__(self, name: str, instructions: str, tools: list = None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
    
    async def run(self, user_input: str) -> str:
        """运行智能体"""
        print(f"[{self.name}] 收到用户输入: {user_input}")
        
        # 模拟LLM处理
        if "天气" in user_input or "weather" in user_input.lower():
            # 提取城市名称
            city = self._extract_city(user_input)
            if city:
                weather_info = await self._get_weather_info(city)
                return weather_info
            else:
                return "请告诉我您想查询哪个城市的天气？"
        else:
            return "我是一个天气智能体，可以帮您查询天气信息。请告诉我您想查询哪个城市的天气？"
    
    def _extract_city(self, text: str) -> Optional[str]:
        """从文本中提取城市名称"""
        cities = ["北京", "上海", "广州", "深圳"]
        for city in cities:
            if city in text:
                return city
        return None
    
    async def _get_weather_info(self, city: str) -> str:
        """获取天气信息"""
        weather_api = WeatherAPI()
        weather = weather_api.get_weather(city)
        
        if weather:
            return f"{city}的天气：温度{weather['temperature']}°C，{weather['condition']}，湿度{weather['humidity']}%"
        else:
            return f"抱歉，暂时无法获取{city}的天气信息"

class Runner:
    """智能体运行器"""
    
    @staticmethod
    async def run(agent: Agent, user_input: str):
        """运行智能体"""
        result = await agent.run(user_input)
        return result

# 工具函数
async def get_weather(location: str) -> str:
    """获取天气信息的工具函数"""
    weather_api = WeatherAPI()
    weather = weather_api.get_weather(location)
    
    if weather:
        return f"Weather in {location}: {weather['temperature']}°C, {weather['condition']}, Humidity: {weather['humidity']}%"
    else:
        return f"Weather information for {location} is not available"

async def save_results(output: str) -> str:
    """保存结果到数据库的工具函数"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[数据库] 保存结果: {output} (时间: {timestamp})")
    return "Results saved successfully"

def main():
    """主函数"""
    print("=== 天气智能体示例 ===\n")
    
    # 创建天气智能体
    weather_agent = Agent(
        name="Weather Agent",
        instructions="You are a helpful agent who can talk to users about the weather.",
        tools=[get_weather, save_results]
    )
    
    # 测试用例
    test_cases = [
        "北京今天天气怎么样？",
        "我想知道上海的天气",
        "广州会下雨吗？",
        "你好，请介绍一下自己",
        "深圳的温度是多少？"
    ]
    
    async def run_tests():
        for i, test_input in enumerate(test_cases, 1):
            print(f"\n--- 测试 {i} ---")
            print(f"用户输入: {test_input}")
            
            try:
                result = await Runner.run(weather_agent, test_input)
                print(f"智能体回复: {result}")
            except Exception as e:
                print(f"错误: {e}")
            
            print("-" * 50)
    
    # 运行测试
    asyncio.run(run_tests())
    
    # 交互式模式
    print("\n=== 交互式模式 ===")
    print("输入 'quit' 退出")
    
    async def interactive_mode():
        while True:
            try:
                user_input = input("\n请输入您的问题: ").strip()
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                
                if user_input:
                    result = await Runner.run(weather_agent, user_input)
                    print(f"智能体: {result}")
                    
            except KeyboardInterrupt:
                print("\n\n再见！")
                break
            except Exception as e:
                print(f"发生错误: {e}")
    
    # 启动交互式模式
    try:
        asyncio.run(interactive_mode())
    except KeyboardInterrupt:
        print("\n\n程序已退出")

if __name__ == "__main__":
    main() 