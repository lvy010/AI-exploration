#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节点创建与链接示例
实现网格搜索中的节点管理
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import math


@dataclass
class Node:
    """网格节点类"""
    x: int              # X坐标
    y: int              # Y坐标
    cost: float         # 从起点到当前节点的成本
    parent_index: int   # 父节点的索引ID
    
    def __post_init__(self):
        """节点创建后的初始化"""
        self.id = self._generate_id()
    
    def _generate_id(self) -> int:
        """生成唯一的节点ID"""
        # 使用坐标和成本生成唯一ID
        return hash((self.x, self.y, self.cost)) % 10000
    
    def get_position(self) -> Tuple[int, int]:
        """获取节点位置"""
        return (self.x, self.y)
    
    def distance_to(self, other: 'Node') -> float:
        """计算到另一个节点的欧几里得距离"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


class NodeManager:
    """节点管理器"""
    
    def __init__(self):
        self.nodes: List[Node] = []
        self.node_id_counter = 0
    
    def create_node(self, x: int, y: int, cost: float, parent_index: int = -1) -> Node:
        """创建新节点"""
        node = Node(x, y, cost, parent_index)
        node.id = self.node_id_counter
        self.node_id_counter += 1
        self.nodes.append(node)
        return node
    
    def get_node_by_id(self, node_id: int) -> Optional[Node]:
        """根据ID获取节点"""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
    
    def get_neighbors(self, node: Node) -> List[Node]:
        """获取节点的相邻节点（8方向）"""
        neighbors = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            # 检查是否已存在该位置的节点
            existing_node = self._get_node_at_position(new_x, new_y)
            if existing_node is None:
                # 创建新相邻节点
                neighbor_cost = node.cost + math.sqrt(dx*dx + dy*dy)  # 对角线距离
                neighbor = self.create_node(new_x, new_y, neighbor_cost, node.id)
                neighbors.append(neighbor)
            else:
                neighbors.append(existing_node)
        
        return neighbors
    
    def _get_node_at_position(self, x: int, y: int) -> Optional[Node]:
        """获取指定位置的节点"""
        for node in self.nodes:
            if node.x == x and node.y == y:
                return node
        return None
    
    def print_node_info(self, node: Node):
        """打印节点信息"""
        print(f"节点ID: {node.id}, 位置: ({node.x}, {node.y}), "
              f"成本: {node.cost:.2f}, 父节点: {node.parent_index}")


def basic_node_creation_example():
    """基本节点创建示例"""
    print("=== 基本节点创建示例 ===")
    
    # 创建节点管理器
    manager = NodeManager()
    
    # 在网格(0,0)创建起点节点，成本0，无父节点(-1)
    start_node = manager.create_node(0, 0, 0.0, -1)
    
    # 从起点移动到相邻节点(1,0)
    # 假设起点节点的唯一ID是100
    # 移动到(1,0)的成本增加1.0
    neighbor_node = manager.create_node(1, 0, start_node.cost + 1.0, start_node.id)
    
    print(f"起点节点: ({start_node.x}, {start_node.y}), 成本: {start_node.cost}, 父节点: {start_node.parent_index}")
    print(f"相邻节点: ({neighbor_node.x}, {neighbor_node.y}), 成本: {neighbor_node.cost}, 父节点: {neighbor_node.parent_index}")
    
    return manager, start_node, neighbor_node


def grid_search_example():
    """网格搜索示例"""
    print("\n=== 网格搜索示例 ===")
    
    manager = NodeManager()
    
    # 创建起点
    start = manager.create_node(0, 0, 0.0, -1)
    print(f"创建起点: {start.get_position()}")
    
    # 获取起点的所有相邻节点
    neighbors = manager.get_neighbors(start)
    print(f"起点有 {len(neighbors)} 个相邻节点:")
    
    for i, neighbor in enumerate(neighbors):
        manager.print_node_info(neighbor)
    
    # 从第一个相邻节点继续扩展
    if neighbors:
        first_neighbor = neighbors[0]
        print(f"\n从节点 {first_neighbor.id} 继续扩展:")
        
        second_level = manager.get_neighbors(first_neighbor)
        for neighbor in second_level:
            manager.print_node_info(neighbor)
    
    return manager


def path_tracking_example():
    """路径跟踪示例"""
    print("\n=== 路径跟踪示例 ===")
    
    manager = NodeManager()
    
    # 创建一条路径: (0,0) -> (1,0) -> (2,1) -> (3,2)
    path_nodes = []
    
    # 起点
    current_node = manager.create_node(0, 0, 0.0, -1)
    path_nodes.append(current_node)
    
    # 路径点
    path_coords = [(1, 0), (2, 1), (3, 2)]
    for x, y in path_coords:
        current_node = manager.create_node(x, y, current_node.cost + 1.0, current_node.id)
        path_nodes.append(current_node)
    
    # 打印完整路径
    print("完整路径:")
    for i, node in enumerate(path_nodes):
        print(f"步骤 {i}: 位置({node.x}, {node.y}), 成本: {node.cost:.2f}, 父节点: {node.parent_index}")
    
    # 从终点回溯到起点
    print("\n路径回溯:")
    current = path_nodes[-1]
    path_back = []
    
    while current.parent_index != -1:
        path_back.append(current)
        current = manager.get_node_by_id(current.parent_index)
        if current is None:
            break
    
    path_back.append(current)  # 添加起点
    
    for i, node in enumerate(reversed(path_back)):
        print(f"回溯 {i}: 位置({node.x}, {node.y})")


def node_statistics():
    """节点统计信息"""
    print("\n=== 节点统计信息 ===")
    
    manager = NodeManager()
    
    # 创建一些测试节点
    test_positions = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0)]
    nodes = []
    
    for i, (x, y) in enumerate(test_positions):
        cost = i * 1.5
        parent_id = -1 if i == 0 else nodes[i-1].id
        node = manager.create_node(x, y, cost, parent_id)
        nodes.append(node)
    
    # 统计信息
    print(f"总节点数: {len(manager.nodes)}")
    print(f"节点ID范围: 0 到 {manager.node_id_counter - 1}")
    
    # 计算平均成本
    total_cost = sum(node.cost for node in manager.nodes)
    avg_cost = total_cost / len(manager.nodes)
    print(f"平均成本: {avg_cost:.2f}")
    
    # 显示所有节点
    print("\n所有节点:")
    for node in manager.nodes:
        manager.print_node_info(node)


if __name__ == "__main__":
    # 运行基本示例
    basic_node_creation_example()
    
    # 运行网格搜索示例
    grid_search_example()
    
    # 运行路径跟踪示例
    path_tracking_example()
    
    # 运行节点统计
    node_statistics()
    
    print("\n=== 节点创建与链接示例完成 ===") 