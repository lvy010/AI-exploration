# 滑动窗口故事生成器

基于提示词管理的连贯叙事生成系统，参考 [1Prompt1Story](https://github.com/byliutao/1Prompt1Story) 项目实现。

## 项目概述

本项目实现了一个智能的故事生成系统，通过滑动窗口技术管理提示词，确保生成的故事具有连贯性和流畅性。

## 核心特性

### 1. 最大窗口长度计算
防止提示词过长，确保在模型的token限制内工作：
```python
def get_max_window_length(unet_controller, id_prompt, frame_prompt_list):
    combined_prompt = id_prompt
    max_len = 0
    for prompt in frame_prompt_list:
        combined_prompt += ' ' + prompt
        if len(combined_prompt.split()) >= 77:  # 标准token限制
            break
        max_len += 1
    return max_len
```

### 2. 循环滑动窗口生成
实现提示词的循环滑动，确保故事连贯性：
```python
def circular_sliding_windows(lst, w):
    n = len(lst)
    return [ [lst[(i+j)%n] for j in range(w)] for i in range(n) ]
```

### 3. 核心生成逻辑
智能管理提示词权重，生成连贯的故事序列：
```python
def movement_gen_story_slide_windows(id_prompt, frame_list, pipe, window_len, seed, controller, save_dir):
    # 计算可用窗口长度
    max_win = get_max_window_length(controller, id_prompt, frame_list)
    window_len = min(window_len, max_win)
    
    # 生成提示窗口
    prompt_windows = circular_sliding_windows(frame_list, window_len)
    
    story_images = []
    for idx, window in enumerate(prompt_windows):
        # 配置提示词权重
        controller.frame_prompt_express = window[0]
        controller.frame_prompt_suppress = window[1:]
        
        # 生成组合提示词
        full_prompt = f"{id_prompt} {' '.join(window)}"
        # 调用生成管线
        image = pipe(full_prompt, generator=torch.Generator().manual_seed(seed)).images[0]
        story_images.append(image)
    
    # 合成输出
    return combine_story(story_images)
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 运行演示版本（推荐）
演示版本不依赖大型模型，可以快速测试核心逻辑：

```bash
python story_generator_demo.py
```

### 2. 运行完整版本
完整版本需要安装扩散模型：

```bash
python story_generator.py
```

## 项目结构

```
story_generator/
├── story_generator.py          # 完整版本（需要扩散模型）
├── story_generator_demo.py     # 演示版本（无需模型）
├── requirements.txt            # 依赖文件
├── README.md                   # 项目说明
└── output/                     # 输出目录
    ├── frame_000.png          # 生成的帧图像
    ├── frame_000_info.txt     # 帧信息
    ├── story_combined.png     # 合成图像
    └── story_video.mp4        # 视频文件
```

## 关键技术点

### 1. 提示词管理
- **身份提示词（ID Prompt）**：定义故事主角或核心元素
- **帧提示词（Frame Prompts）**：定义每个场景的具体内容
- **表达提示词（Express）**：当前帧的主要表达内容
- **抑制提示词（Suppress）**：需要抑制的次要内容

### 2. 滑动窗口机制
- **窗口大小**：控制每帧包含的提示词数量
- **循环滑动**：确保故事的连续性和完整性
- **权重分配**：智能分配提示词的重要性

### 3. 连贯性保证
- **重叠检测**：计算相邻帧之间的提示词重叠度
- **流程分析**：分析故事的整体连贯性
- **质量控制**：确保生成内容的质量和一致性

## 示例输出

### 故事流程示例
```
身份提示词: 一个勇敢的年轻骑士
帧提示词: ['在森林中骑马前行', '发现一座古老的城堡', '进入城堡探索', ...]

窗口 1: ['在森林中骑马前行', '发现一座古老的城堡', '进入城堡探索']
窗口 2: ['发现一座古老的城堡', '进入城堡探索', '遇到神秘的魔法师']
窗口 3: ['进入城堡探索', '遇到神秘的魔法师', '与魔法师交谈']
...
```

### 连贯性分析
```
帧 1 -> 帧 2 重叠: 2 个提示词
帧 2 -> 帧 3 重叠: 2 个提示词
平均重叠度: 2.00
```

## 配置参数

- **窗口长度**：建议设置为2-4，平衡连贯性和多样性
- **随机种子**：控制生成结果的随机性
- **模型选择**：支持各种Stable Diffusion模型
- **生成参数**：可调整推理步数、引导尺度等

## 扩展功能

1. **视频生成**：将生成的图像序列合成为视频
2. **多模态支持**：支持文本、图像等多种输入
3. **风格控制**：支持不同的艺术风格和表现手法
4. **批量处理**：支持批量生成多个故事

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

MIT License

## 致谢

感谢 [1Prompt1Story](https://github.com/byliutao/1Prompt1Story) 项目的启发和参考。 