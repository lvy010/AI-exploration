#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑动窗口故事生成器
基于提示词管理的连贯叙事生成系统
"""

import torch
import numpy as np
from PIL import Image
import cv2
from typing import List, Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class UNetController:
    """UNet控制器，管理提示词权重"""
    frame_prompt_express: str = ""
    frame_prompt_suppress: List[str] = None
    
    def __post_init__(self):
        if self.frame_prompt_suppress is None:
            self.frame_prompt_suppress = []


class StoryGenerator:
    """故事生成器主类"""
    
    def __init__(self, model_name: str = "runwayml/stable-diffusion-v1-5"):
        """
        初始化故事生成器
        
        Args:
            model_name: 使用的扩散模型名称
        """
        self.model_name = model_name
        self.pipe = None
        self.controller = UNetController()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"使用设备: {self.device}")
        print(f"模型: {model_name}")
    
    def load_model(self):
        """加载扩散模型"""
        try:
            from diffusers import StableDiffusionPipeline
            
            print("正在加载模型...")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None
            )
            
            if self.device == "cuda":
                self.pipe = self.pipe.to(self.device)
            
            print("模型加载完成！")
            return True
            
        except ImportError:
            print("错误: 请安装 diffusers 库")
            return False
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
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
    
    def generate_frame(self, prompt: str, seed: int, negative_prompt: str = "") -> Image.Image:
        """
        生成单帧图像
        
        Args:
            prompt: 正向提示词
            seed: 随机种子
            negative_prompt: 负向提示词
            
        Returns:
            生成的图像
        """
        if self.pipe is None:
            raise ValueError("模型未加载，请先调用 load_model()")
        
        generator = torch.Generator(device=self.device).manual_seed(seed)
        
        # 应用控制器权重
        if self.controller.frame_prompt_express:
            prompt = f"{prompt} {self.controller.frame_prompt_express}"
        
        if self.controller.frame_prompt_suppress:
            suppress_text = " ".join(self.controller.frame_prompt_suppress)
            negative_prompt = f"{negative_prompt} {suppress_text}".strip()
        
        # 生成图像
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            generator=generator,
            num_inference_steps=20,
            guidance_scale=7.5
        )
        
        return result.images[0]
    
    def movement_gen_story_slide_windows(self, 
                                       id_prompt: str, 
                                       frame_list: List[str], 
                                       window_len: int, 
                                       seed: int, 
                                       save_dir: str = "./output") -> List[Image.Image]:
        """
        核心生成逻辑：滑动窗口故事生成
        
        Args:
            id_prompt: 身份提示词
            frame_list: 帧提示词列表
            window_len: 窗口长度
            seed: 随机种子
            save_dir: 保存目录
            
        Returns:
            生成的故事图像列表
        """
        if self.pipe is None:
            raise ValueError("模型未加载，请先调用 load_model()")
        
        # 计算可用窗口长度
        max_win = self.get_max_window_length(self.controller, id_prompt, frame_list)
        window_len = min(window_len, max_win)
        
        print(f"使用窗口长度: {window_len} (最大可用: {max_win})")
        
        # 生成提示窗口
        prompt_windows = self.circular_sliding_windows(frame_list, window_len)
        
        print(f"生成 {len(prompt_windows)} 个窗口")
        
        story_images = []
        for idx, window in enumerate(prompt_windows):
            print(f"生成第 {idx + 1}/{len(prompt_windows)} 帧...")
            
            # 配置提示词权重
            self.controller.frame_prompt_express = window[0]
            self.controller.frame_prompt_suppress = window[1:]
            
            # 生成组合提示词
            full_prompt = f"{id_prompt} {' '.join(window)}"
            
            # 生成图像
            image = self.generate_frame(full_prompt, seed + idx)
            story_images.append(image)
            
            # 保存单帧
            image.save(f"{save_dir}/frame_{idx:03d}.png")
        
        return story_images
    
    def combine_story(self, images: List[Image.Image], 
                     output_path: str = "./output/story_combined.png") -> Image.Image:
        """
        合成故事图像
        
        Args:
            images: 图像列表
            output_path: 输出路径
            
        Returns:
            合成的图像
        """
        if not images:
            raise ValueError("图像列表为空")
        
        # 计算布局
        n = len(images)
        cols = int(math.ceil(math.sqrt(n)))
        rows = int(math.ceil(n / cols))
        
        # 获取图像尺寸
        img_width, img_height = images[0].size
        
        # 创建画布
        canvas_width = cols * img_width
        canvas_height = rows * img_height
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        
        # 拼接图像
        for idx, img in enumerate(images):
            row = idx // cols
            col = idx % cols
            x = col * img_width
            y = row * img_height
            canvas.paste(img, (x, y))
        
        # 保存合成图像
        canvas.save(output_path)
        print(f"故事合成完成: {output_path}")
        
        return canvas
    
    def create_video(self, image_paths: List[str], 
                    output_path: str = "./output/story_video.mp4", 
                    fps: int = 2) -> str:
        """
        创建视频文件
        
        Args:
            image_paths: 图像路径列表
            output_path: 输出视频路径
            fps: 帧率
            
        Returns:
            视频文件路径
        """
        if not image_paths:
            raise ValueError("图像路径列表为空")
        
        # 读取第一张图像获取尺寸
        first_img = cv2.imread(image_paths[0])
        height, width, layers = first_img.shape
        
        # 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # 写入帧
        for img_path in image_paths:
            img = cv2.imread(img_path)
            video.write(img)
        
        video.release()
        print(f"视频创建完成: {output_path}")
        
        return output_path


def demo_story_generation():
    """演示故事生成"""
    print("=== 滑动窗口故事生成器演示 ===\n")
    
    # 创建生成器
    generator = StoryGenerator()
    
    # 加载模型
    if not generator.load_model():
        print("模型加载失败，退出演示")
        return
    
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
    
    # 生成故事
    try:
        story_images = generator.movement_gen_story_slide_windows(
            id_prompt=id_prompt,
            frame_list=frame_prompts,
            window_len=3,  # 3帧窗口
            seed=42,
            save_dir="./output"
        )
        
        # 合成故事
        combined_image = generator.combine_story(story_images)
        
        print(f"\n故事生成完成！共生成 {len(story_images)} 帧")
        print("输出文件:")
        print("- 单帧图像: ./output/frame_*.png")
        print("- 合成图像: ./output/story_combined.png")
        
    except Exception as e:
        print(f"生成过程中出现错误: {e}")


if __name__ == "__main__":
    demo_story_generation() 