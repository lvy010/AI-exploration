#!/usr/bin/env python3
"""
多智能体翻译管理器示例
演示管理器模式（智能体作为工具）
"""

import asyncio
from typing import Dict, List

# 模拟智能体框架
class Agent:
    """简化的智能体类"""
    
    def __init__(self, name: str, instructions: str, tools: list = None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
    
    def as_tool(self, tool_name: str, tool_description: str):
        """将智能体转换为工具"""
        return {
            "name": tool_name,
            "description": tool_description,
            "agent": self
        }
    
    async def translate(self, text: str, target_language: str) -> str:
        """翻译文本到目标语言"""
        print(f"[{self.name}] 翻译文本: '{text}' 到 {target_language}")
        
        # 模拟翻译
        translations = {
            "Spanish": {
                "hello": "hola",
                "world": "mundo",
                "good morning": "buenos días",
                "thank you": "gracias"
            },
            "French": {
                "hello": "bonjour",
                "world": "monde", 
                "good morning": "bonjour",
                "thank you": "merci"
            },
            "Italian": {
                "hello": "ciao",
                "world": "mondo",
                "good morning": "buongiorno", 
                "thank you": "grazie"
            }
        }
        
        lang_translations = translations.get(target_language, {})
        text_lower = text.lower()
        
        if text_lower in lang_translations:
            return lang_translations[text_lower]
        else:
            return f"[{target_language}] {text}"

class ManagerAgent:
    """管理器智能体"""
    
    def __init__(self, name: str, instructions: str, tools: List[Dict]):
        self.name = name
        self.instructions = instructions
        self.tools = tools
    
    async def process_request(self, user_input: str) -> List[str]:
        """处理用户请求"""
        print(f"[{self.name}] 收到请求: {user_input}")
        
        results = []
        
        # 解析用户请求
        if "translate" in user_input.lower():
            # 提取要翻译的文本和目标语言
            text, languages = self._parse_translation_request(user_input)
            
            if text and languages:
                for language in languages:
                    # 找到对应的翻译工具
                    tool = self._find_translation_tool(language)
                    if tool:
                        translation = await tool["agent"].translate(text, language)
                        results.append(f"{language}: {translation}")
                    else:
                        results.append(f"不支持翻译到 {language}")
            else:
                results.append("请提供要翻译的文本和目标语言")
        
        return results
    
    def _parse_translation_request(self, user_input: str) -> tuple:
        """解析翻译请求"""
        # 简化的解析逻辑
        text = None
        languages = []
        
        # 提取引号中的文本
        import re
        text_match = re.search(r"'([^']+)'", user_input)
        if text_match:
            text = text_match.group(1)
        
        # 提取语言
        if "spanish" in user_input.lower():
            languages.append("Spanish")
        if "french" in user_input.lower():
            languages.append("French")
        if "italian" in user_input.lower():
            languages.append("Italian")
        
        return text, languages
    
    def _find_translation_tool(self, language: str):
        """查找翻译工具"""
        for tool in self.tools:
            if language.lower() in tool["name"].lower():
                return tool
        return None

class Runner:
    """智能体运行器"""
    
    @staticmethod
    async def run(agent, user_input: str):
        """运行智能体"""
        if isinstance(agent, ManagerAgent):
            return await agent.process_request(user_input)
        else:
            return await agent.translate(user_input, "English")

def main():
    """主函数"""
    print("=== 多智能体翻译管理器示例 ===\n")
    
    # 创建专业翻译智能体
    spanish_agent = Agent(
        name="Spanish Translator",
        instructions="You translate text to Spanish accurately and naturally."
    )
    
    french_agent = Agent(
        name="French Translator",
        instructions="You translate text to French accurately and naturally."
    )
    
    italian_agent = Agent(
        name="Italian Translator", 
        instructions="You translate text to Italian accurately and naturally."
    )
    
    # 创建管理器智能体
    manager_agent = ManagerAgent(
        name="Translation Manager",
        instructions="You are a translation agent. You use the tools given to you to translate. If asked for multiple translations, you call the relevant tools.",
        tools=[
            spanish_agent.as_tool(
                tool_name="translate_to_spanish",
                tool_description="Translate the user's message to Spanish"
            ),
            french_agent.as_tool(
                tool_name="translate_to_french",
                tool_description="Translate the user's message to French"
            ),
            italian_agent.as_tool(
                tool_name="translate_to_italian",
                tool_description="Translate the user's message to Italian"
            )
        ]
    )
    
    # 测试用例
    test_cases = [
        "Translate 'hello' to Spanish, French and Italian for me!",
        "Translate 'world' to Spanish",
        "Translate 'thank you' to French and Italian",
        "What languages can you translate to?",
        "Translate 'good morning' to all languages"
    ]
    
    async def run_tests():
        for i, test_input in enumerate(test_cases, 1):
            print(f"\n--- 测试 {i} ---")
            print(f"用户输入: {test_input}")
            
            try:
                results = await Runner.run(manager_agent, test_input)
                print("翻译结果:")
                for result in results:
                    print(f"  - {result}")
            except Exception as e:
                print(f"错误: {e}")
            
            print("-" * 50)
    
    # 运行测试
    asyncio.run(run_tests())
    
    # 交互式模式
    print("\n=== 交互式模式 ===")
    print("输入 'quit' 退出")
    print("示例: Translate 'hello' to Spanish, French and Italian")
    
    async def interactive_mode():
        while True:
            try:
                user_input = input("\n请输入翻译请求: ").strip()
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("再见！")
                    break
                
                if user_input:
                    results = await Runner.run(manager_agent, user_input)
                    print("\n翻译结果:")
                    for result in results:
                        print(f"  - {result}")
                    
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