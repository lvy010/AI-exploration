#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑动窗口故事生成器演示版
展示核心逻辑，不依赖大型模型
"""

import math
from typing import List
from dataclasses import dataclass
import os


@dataclass
class UNetController:
    """UNet控制器，管理提示词权重"""
    frame_prompt_express: str = ""
    frame_prompt_suppress: List[str] = None
    
    def __post_init__(self):
        if self.frame_prompt_suppress is None:
            self.frame_prompt_suppress = []


class StoryGeneratorDemo:
    """故事生成器演示版"""
    
    def __init__(self):
        self.controller = UNetController()
    
    def get_max_window_length(self, id_prompt: str, frame_prompt_list: List[str]) -> int:
        """
        计算最大窗口长度（防止提示词过长）
        
        Args:
            id_prompt: 身份提示词
            frame_prompt_list: 帧提示词列表
            
        Returns:
            最大可用窗口长度
        """
        combined_prompt = id_prompt
        max_len = 0
        
        for prompt in frame_prompt_list:
            combined_prompt += ' ' + prompt
            if len(combined_prompt.split()) >= 77:  # 标准token限制
                break
            max_len += 1
        
        return max_len
    
    def circular_sliding_windows(self, lst: List, w: int) -> List[List]:
        """
        循环滑动窗口生成
        
        Args:
            lst: 输入列表
            w: 窗口大小
            
        Returns:
            滑动窗口列表
        """
        n = len(lst)
        if n == 0:
            return []
        
        windows = []
        for i in range(n):
            window = []
            for j in range(w):
                window.append(lst[(i + j) % n])
            windows.append(window)
        
        return windows
    
    def movement_gen_story_slide_windows(self, 
                                       id_prompt: str, 
                                       frame_list: List[str], 
                                       window_len: int, 
                                       seed: int, 
                                       save_dir: str = "./output") -> List[dict]:
        """
        核心生成逻辑：滑动窗口故事生成（演示版）
        
        Args:
            id_prompt: 身份提示词
            frame_list: 帧提示词列表
            window_len: 窗口长度
            seed: 随机种子
            save_dir: 保存目录
            
        Returns:
            生成的故事帧信息列表
        """
        # 计算可用窗口长度
        max_win = self.get_max_window_length(self.controller, id_prompt, frame_list)
        window_len = min(window_len, max_win)
        
        print(f"使用窗口长度: {window_len} (最大可用: {max_win})")
        
        # 生成提示窗口
        prompt_windows = self.circular_sliding_windows(frame_list, window_len)
        
        print(f"生成 {len(prompt_windows)} 个窗口")
        
        story_frames = []
        for idx, window in enumerate(prompt_windows):
            print(f"生成第 {idx + 1}/{len(prompt_windows)} 帧...")
            
            # 配置提示词权重
            self.controller.frame_prompt_express = window[0]
            self.controller.frame_prompt_suppress = window[1:]
            
            # 生成组合提示词
            full_prompt = f"{id_prompt} {' '.join(window)}"
            
            # 模拟生成结果
            frame_info = {
                'frame_id': idx,
                'window': window,
                'express_prompt': self.controller.frame_prompt_express,
                'suppress_prompts': self.controller.frame_prompt_suppress,
                'full_prompt': full_prompt,
                'seed': seed + idx,
                'simulated_image_path': f"{save_dir}/frame_{idx:03d}.png"
            }
            
            story_frames.append(frame_info)
            
            # 保存提示词信息到文件
            self.save_frame_info(frame_info, save_dir, idx)
        
        return story_frames
    
    def save_frame_info(self, frame_info: dict, save_dir: str, idx: int):
        """保存帧信息到文件"""
        os.makedirs(save_dir, exist_ok=True)
        
        info_file = f"{save_dir}/frame_{idx:03d}_info.txt"
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"帧ID: {frame_info['frame_id']}\n")
            f.write(f"窗口内容: {frame_info['window']}\n")
            f.write(f"表达提示词: {frame_info['express_prompt']}\n")
            f.write(f"抑制提示词: {frame_info['suppress_prompts']}\n")
            f.write(f"完整提示词: {frame_info['full_prompt']}\n")
            f.write(f"随机种子: {frame_info['seed']}\n")
            f.write(f"图像路径: {frame_info['simulated_image_path']}\n")
    
    def analyze_story_flow(self, story_frames: List[dict]):
        """分析故事流程"""
        print("\n=== 故事流程分析 ===")
        
        for i, frame in enumerate(story_frames):
            print(f"\n帧 {i+1}:")
            print(f"  窗口: {frame['window']}")
            print(f"  表达: {frame['express_prompt']}")
            print(f"  抑制: {frame['suppress_prompts']}")
            print(f"  完整提示词: {frame['full_prompt'][:80]}...")
        
        # 分析连贯性
        print(f"\n=== 连贯性分析 ===")
        print(f"总帧数: {len(story_frames)}")
        print(f"窗口大小: {len(story_frames[0]['window']) if story_frames else 0}")
        
        # 计算提示词重叠度
        if len(story_frames) > 1:
            overlap_count = 0
            for i in range(len(story_frames) - 1):
                current_window = set(story_frames[i]['window'])
                next_window = set(story_frames[i + 1]['window'])
                overlap = len(current_window & next_window)
                overlap_count += overlap
                print(f"  帧 {i+1} -> 帧 {i+2} 重叠: {overlap} 个提示词")
            
            avg_overlap = overlap_count / (len(story_frames) - 1)
            print(f"平均重叠度: {avg_overlap:.2f}")


def demo_basic_functionality():
    """演示基本功能"""
    print("=== 滑动窗口故事生成器演示 ===\n")
    
    # 创建生成器
    generator = StoryGeneratorDemo()
    
    # 示例数据
    id_prompt = "一个勇敢的年轻骑士"
    frame_prompts = [
        "在森林中骑马前行",
        "发现一座古老的城堡",
        "进入城堡探索",
        "遇到神秘的魔法师",
        "与魔法师交谈",
        "获得神秘的魔法剑",
        "离开城堡继续冒险",
        "在夕阳下骑马回家"
    ]
    
    print(f"身份提示词: {id_prompt}")
    print(f"帧提示词数量: {len(frame_prompts)}")
    print(f"帧提示词列表: {frame_prompts}")
    
    # 测试最大窗口长度计算
    max_len = generator.get_max_window_length(id_prompt, frame_prompts)
    print(f"\n最大可用窗口长度: {max_len}")
    
    # 测试滑动窗口生成
    window_len = 3
    windows = generator.circular_sliding_windows(frame_prompts, window_len)
    print(f"\n滑动窗口 (窗口大小={window_len}):")
    for i, window in enumerate(windows):
        print(f"  窗口 {i+1}: {window}")
    
    # 生成故事
    print(f"\n=== 开始生成故事 ===")
    story_frames = generator.movement_gen_story_slide_windows(
        id_prompt=id_prompt,
        frame_list=frame_prompts,
        window_len=window_len,
        seed=42,
        save_dir="./output"
    )
    
    # 分析故事流程
    generator.analyze_story_flow(story_frames)
    
    print(f"\n=== 生成完成 ===")
    print(f"共生成 {len(story_frames)} 帧")
    print("输出文件:")
    print("- 帧信息: ./output/frame_*_info.txt")
    print("- 模拟图像路径: ./output/frame_*.png")


def demo_different_window_sizes():
    """演示不同窗口大小的效果"""
    print("\n\n=== 不同窗口大小对比演示 ===")
    
    generator = StoryGeneratorDemo()
    
    id_prompt = "一只可爱的小猫"
    frame_prompts = [
        "在花园里玩耍",
        "追逐蝴蝶",
        "爬上树",
        "在阳光下休息",
        "回家吃晚饭"
    ]
    
    window_sizes = [2, 3, 4]
    
    for window_size in window_sizes:
        print(f"\n--- 窗口大小: {window_size} ---")
        
        # 计算最大可用长度
        max_len = generator.get_max_window_length(id_prompt, frame_prompts)
        actual_window_size = min(window_size, max_len)
        
        # 生成窗口
        windows = generator.circular_sliding_windows(frame_prompts, actual_window_size)
        
        print(f"实际窗口大小: {actual_window_size}")
        print(f"生成窗口数: {len(windows)}")
        
        for i, window in enumerate(windows):
            print(f"  窗口 {i+1}: {window}")


if __name__ == "__main__":
    # 基本功能演示
    demo_basic_functionality()
    
    # 不同窗口大小演示
    demo_different_window_sizes()
    
    print("\n=== 演示完成 ===") 