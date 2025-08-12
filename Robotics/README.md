# 机器人运动仿真模块

这个模块实现了基于自行车模型的机器人运动仿真，可以模拟机器人在不同控制输入下的运动轨迹。

## 功能特性

- **自行车运动模型**: 基于阿克曼转向几何的运动学模型
- **多步运动仿真**: 支持长时间的运动轨迹仿真
- **多种运动模式**: 直线运动、转弯、加速减速等
- **轨迹分析**: 提供轨迹统计和分析功能

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本仿真

运行基本的三秒运动仿真：

```bash
python robot_motion_simulation.py
```

### 代码示例

```python
from robot_motion_simulation import State, update_motion_model
import math

# 创建初始状态
initial_state = State(x=0.0, y=0.0, yaw=math.radians(0), v=0.0)

# 施加控制输入
accel_cmd = 0.5  # 加速度 (m/s²)
steer_cmd = math.radians(5.0)  # 转向角 (rad)

# 更新状态
new_state = update_motion_model(initial_state, accel_cmd, steer_cmd)
```

## 输出示例

```
=== 机器人运动仿真 ===
观察机器人多步运动：

初始状态: X=0.00, Y=0.00, Yaw=0.00°, V=0.00 m/s

--- 运动仿真 ---
时间: 1.0s | X=0.05, Y=0.00, Yaw=0.02°, V=0.50 m/s
时间: 2.0s | X=0.20, Y=0.01, Yaw=0.05°, V=1.00 m/s
时间: 3.0s | X=0.45, Y=0.03, Yaw=0.09°, V=1.50 m/s

3.0秒后最终状态:
X=0.45, Y=0.03, Yaw=0.09°, V=1.50 m/s
```

## 模型参数

- **轴距 (L)**: 2.0 米
- **时间步长 (dt)**: 0.1 秒
- **最大转向角**: ±30°

## 运动模式

1. **直线加速**: 恒定加速度，零转向角
2. **匀速转弯**: 恒定速度，恒定转向角
3. **减速**: 负加速度
4. **复杂轨迹**: 组合多种运动模式

## 文件结构

```
Robotics/
├── robot_motion_simulation.py  # 主仿真模块
├── requirements.txt            # 依赖包列表
└── README.md                  # 说明文档
```

## 扩展功能

- 添加可视化功能（matplotlib）
- 支持更复杂的运动模型
- 添加障碍物避障功能
- 实现路径规划算法 
 