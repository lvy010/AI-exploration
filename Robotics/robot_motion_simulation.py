#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器人运动仿真模块
实现基于自行车模型的机器人运动仿真
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class State:
    """机器人状态类"""
    x: float      # X坐标 (m)
    y: float      # Y坐标 (m)
    yaw: float    # 偏航角 (rad)
    v: float      # 线速度 (m/s)


def update_motion_model(state: State, accel: float, steer: float, dt: float = 0.1) -> State:
    """
    更新机器人运动模型（自行车模型）
    
    参数:
        state: 当前状态
        accel: 加速度 (m/s²)
        steer: 转向角 (rad)
        dt: 时间步长 (s)
    
    返回:
        更新后的状态
    """
    # 自行车模型参数
    L = 2.0  # 轴距 (m)
    
    # 当前状态
    x = state.x
    y = state.y
    yaw = state.yaw
    v = state.v
    
    # 运动学更新
    new_v = v + accel * dt
    new_v = max(0, new_v)  # 速度不能为负
    
    # 计算角速度
    omega = (new_v * math.tan(steer)) / L
    
    # 更新位置和姿态
    new_x = x + new_v * math.cos(yaw) * dt
    new_y = y + new_v * math.sin(yaw) * dt
    new_yaw = yaw + omega * dt
    
    # 归一化偏航角到 [-π, π]
    new_yaw = math.atan2(math.sin(new_yaw), math.cos(new_yaw))
    
    return State(x=new_x, y=new_y, yaw=new_yaw, v=new_v)


def simulate_robot_motion():
    """机器人运动仿真主函数"""
    print("=== 机器人运动仿真 ===")
    print("观察机器人多步运动：\n")
    
    # 创建初始状态
    initial_state = State(x=0.0, y=0.0, yaw=math.radians(0), v=0.0)
    print(f"初始状态: X={initial_state.x:.2f}, Y={initial_state.y:.2f}, "
          f"Yaw={math.degrees(initial_state.yaw):.2f}°, V={initial_state.v:.2f} m/s")
    
    # 仿真参数
    dt = 0.1  # 时间步长
    current_time = 0.0
    total_sim_time = 3.0
    current_state = initial_state
    
    print("\n--- 运动仿真 ---")
    
    # 3秒仿真循环
    while current_time < total_sim_time:
        # 施加恒定加速度和小转向角
        accel_cmd = 0.5  # m/s²（加速）
        steer_cmd = math.radians(5.0)  # 5°（温和右转）
        
        # 更新机器人状态
        current_state = update_motion_model(current_state, accel_cmd, steer_cmd, dt)
        
        current_time += dt
        # 演示时每秒打印一次
        if int(current_time * 10) % 10 == 0:
            print(f"时间: {current_time:.1f}s | "
                  f"X={current_state.x:.2f}, Y={current_state.y:.2f}, "
                  f"Yaw={math.degrees(current_state.yaw):.2f}°, V={current_state.v:.2f} m/s")
    
    print(f"\n{total_sim_time:.1f}秒后最终状态:")
    print(f"X={current_state.x:.2f}, Y={current_state.y:.2f}, "
          f"Yaw={math.degrees(current_state.yaw):.2f}°, V={current_state.v:.2f} m/s")


def advanced_simulation():
    """高级仿真：不同运动模式"""
    print("\n\n=== 高级运动仿真 ===")
    print("测试不同的运动模式：\n")
    
    # 初始状态
    state = State(x=0.0, y=0.0, yaw=0.0, v=0.0)
    dt = 0.1
    time = 0.0
    
    # 运动模式定义：(时间, 加速度, 转向角)
    motion_patterns = [
        (1.0, 1.0, 0.0),      # 直线加速
        (2.0, 0.0, math.radians(10)),  # 匀速右转
        (1.0, -0.5, 0.0),     # 减速
        (1.0, 0.0, math.radians(-15))  # 左转
    ]
    
    print("时间(s) | X(m)  | Y(m)  | Yaw(°) | V(m/s) | 动作")
    print("-" * 60)
    
    for duration, accel, steer in motion_patterns:
        end_time = time + duration
        
        while time < end_time:
            state = update_motion_model(state, accel, steer, dt)
            time += dt
            
            # 每0.5秒打印一次
            if int(time * 2) % 2 == 0:
                action = f"a={accel:.1f}, δ={math.degrees(steer):.1f}°"
                print(f"{time:6.1f} | {state.x:5.2f} | {state.y:5.2f} | "
                      f"{math.degrees(state.yaw):6.1f} | {state.v:5.2f} | {action}")


def trajectory_analysis():
    """轨迹分析"""
    print("\n\n=== 轨迹分析 ===")
    
    # 记录轨迹点
    trajectory = []
    state = State(x=0.0, y=0.0, yaw=0.0, v=0.0)
    dt = 0.1
    time = 0.0
    
    # 圆形轨迹仿真
    print("生成圆形轨迹...")
    while time < 10.0:
        trajectory.append((state.x, state.y))
        
        # 恒定速度，恒定转向角
        accel = 0.0
        steer = math.radians(5.0)  # 5度转向
        
        state = update_motion_model(state, accel, steer, dt)
        time += dt
    
    # 计算轨迹统计
    x_coords = [p[0] for p in trajectory]
    y_coords = [p[1] for p in trajectory]
    
    print(f"轨迹总长度: {len(trajectory)} 个点")
    print(f"X范围: [{min(x_coords):.2f}, {max(x_coords):.2f}]")
    print(f"Y范围: [{min(y_coords):.2f}, {max(y_coords):.2f}]")
    print(f"最终位置: ({state.x:.2f}, {state.y:.2f})")


if __name__ == "__main__":
    # 运行基本仿真
    simulate_robot_motion()
    
    # 运行高级仿真
    advanced_simulation()
    
    # 运行轨迹分析
    trajectory_analysis()
    
    print("\n=== 仿真完成 ===") 