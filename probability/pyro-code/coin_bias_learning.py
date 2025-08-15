#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
硬币偏置学习示例
使用Pyro实现贝叶斯推断，学习硬币的偏置概率
"""

import pyro
import pyro.distributions as dist
import pyro.optim as optim
from pyro.infer import SVI, Trace_ELBO
import torch
import matplotlib.pyplot as plt
import numpy as np


def coin_model(data):
    """
    定义生成模型
    硬币偏置p的Beta先验及观测数据生成过程
    """
    # 使用Beta(1,1)作为均匀先验
    p = pyro.sample("p", dist.Beta(1.0, 1.0))
    
    # 对每个观测数据点进行采样
    with pyro.plate("data_loop", len(data)):
        pyro.sample("obs", dist.Bernoulli(p), obs=data)


def coin_guide(data):
    """
    构建引导函数（变分后验）
    使用可学习的Beta分布参数alpha和beta近似后验
    """
    # 可学习的参数，约束为正数
    alpha = pyro.param("guide_alpha", torch.tensor(1.0), 
                      constraint=dist.constraints.positive)
    beta = pyro.param("guide_beta", torch.tensor(1.0),
                     constraint=dist.constraints.positive)
    
    # 从变分后验采样
    pyro.sample("p", dist.Beta(alpha, beta))


def run_basic_inference():
    """运行基本贝叶斯推断"""
    print("=== 硬币偏置学习示例 ===")
    print("观测数据：10次投掷，8次正面，2次反面\n")
    
    # 观测数据（8次正面，2次反面）
    observed_data = torch.tensor([1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0])
    
    print(f"观测数据: {observed_data.tolist()}")
    print(f"正面次数: {observed_data.sum().item()}")
    print(f"反面次数: {len(observed_data) - observed_data.sum().item()}")
    print(f"经验概率: {observed_data.mean().item():.2f}")
    
    # 初始化环境
    pyro.clear_param_store()
    
    # 设置优化器和损失函数
    adam = optim.Adam({"lr": 0.01})
    elbo = Trace_ELBO()
    svi = SVI(coin_model, coin_guide, adam, elbo)
    
    # 执行训练
    print("\n开始训练...")
    losses = []
    for i in range(1000):
        loss = svi.step(observed_data)
        losses.append(loss)
        
        if i % 100 == 0:
            print(f"迭代 {i:3d}, 损失: {loss:.4f}")
    
    # 输出学习结果
    alpha_learned = pyro.param("guide_alpha").item()
    beta_learned = pyro.param("guide_beta").item()
    inferred_prob = alpha_learned / (alpha_learned + beta_learned)
    
    print(f"\n=== 学习结果 ===")
    print(f"学习参数: alpha={alpha_learned:.3f}, beta={beta_learned:.3f}")
    print(f"推断正面概率: {inferred_prob:.3f}")
    print(f"理论后验均值: {(1 + 8) / (1 + 1 + 10):.3f}")  # Beta(1+8, 1+2)的均值
    
    return alpha_learned, beta_learned, losses


def advanced_analysis(alpha, beta):
    """高级分析：后验分布可视化"""
    print("\n=== 后验分布分析 ===")
    
    # 生成后验分布样本
    posterior = dist.Beta(alpha, beta)
    samples = posterior.sample((10000,))
    
    # 计算统计量
    mean_prob = samples.mean().item()
    std_prob = samples.std().item()
    credible_interval_95 = torch.quantile(samples, torch.tensor([0.025, 0.975]))
    
    print(f"后验均值: {mean_prob:.3f}")
    print(f"后验标准差: {std_prob:.3f}")
    print(f"95%置信区间: [{credible_interval_95[0]:.3f}, {credible_interval_95[1]:.3f}]")
    
    return samples, credible_interval_95


def compare_priors():
    """比较不同先验的影响"""
    print("\n=== 不同先验比较 ===")
    
    # 观测数据
    observed_data = torch.tensor([1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0])
    
    # 不同先验设置
    priors = [
        ("均匀先验 Beta(1,1)", 1.0, 1.0),
        ("弱信息先验 Beta(2,2)", 2.0, 2.0),
        ("强信息先验 Beta(10,10)", 10.0, 10.0),
        ("偏正面先验 Beta(5,1)", 5.0, 1.0),
        ("偏反面先验 Beta(1,5)", 1.0, 5.0)
    ]
    
    results = []
    
    for prior_name, alpha_prior, beta_prior in priors:
        print(f"\n{prior_name}:")
        
        # 重新定义模型和引导函数
        def coin_model_with_prior(data):
            p = pyro.sample("p", dist.Beta(alpha_prior, beta_prior))
            with pyro.plate("data_loop", len(data)):
                pyro.sample("obs", dist.Bernoulli(p), obs=data)
        
        def coin_guide_with_prior(data):
            alpha = pyro.param(f"guide_alpha_{alpha_prior}_{beta_prior}", 
                             torch.tensor(1.0), 
                             constraint=dist.constraints.positive)
            beta = pyro.param(f"guide_beta_{alpha_prior}_{beta_prior}",
                            torch.tensor(1.0),
                            constraint=dist.constraints.positive)
            pyro.sample("p", dist.Beta(alpha, beta))
        
        # 训练
        pyro.clear_param_store()
        adam = optim.Adam({"lr": 0.01})
        elbo = Trace_ELBO()
        svi = SVI(coin_model_with_prior, coin_guide_with_prior, adam, elbo)
        
        for i in range(500):  # 减少迭代次数
            svi.step(observed_data)
        
        # 获取结果
        alpha_learned = pyro.param(f"guide_alpha_{alpha_prior}_{beta_prior}").item()
        beta_learned = pyro.param(f"guide_beta_{alpha_prior}_{beta_prior}").item()
        inferred_prob = alpha_learned / (alpha_learned + beta_learned)
        
        print(f"  推断概率: {inferred_prob:.3f}")
        results.append((prior_name, inferred_prob))
    
    return results


def simulate_predictions(alpha, beta, n_simulations=1000):
    """模拟预测未来投掷结果"""
    print(f"\n=== 预测分析 ===")
    print(f"基于学习到的后验分布，模拟{n_simulations}次未来投掷:")
    
    # 从后验分布采样
    posterior = dist.Beta(alpha, beta)
    p_samples = posterior.sample((n_simulations,))
    
    # 模拟未来投掷
    future_tosses = dist.Bernoulli(p_samples).sample((10,)).t()  # 每次10个投掷
    
    # 统计结果
    heads_counts = future_tosses.sum(dim=1)
    
    print(f"平均正面次数: {heads_counts.float().mean():.2f}")
    print(f"正面次数分布:")
    for i in range(11):
        count = (heads_counts == i).sum().item()
        print(f"  {i}次正面: {count:4d}次 ({count/n_simulations*100:5.1f}%)")


def plot_results(alpha, beta, samples, losses):
    """绘制结果图表"""
    try:
        plt.figure(figsize=(15, 10))
        
        # 子图1: 损失曲线
        plt.subplot(2, 3, 1)
        plt.plot(losses)
        plt.title('训练损失曲线')
        plt.xlabel('迭代次数')
        plt.ylabel('ELBO损失')
        plt.grid(True)
        
        # 子图2: 后验分布
        plt.subplot(2, 3, 2)
        plt.hist(samples.numpy(), bins=50, density=True, alpha=0.7, color='skyblue')
        plt.axvline(alpha/(alpha+beta), color='red', linestyle='--', 
                   label=f'后验均值: {alpha/(alpha+beta):.3f}')
        plt.axvline(0.8, color='green', linestyle='--', 
                   label='经验概率: 0.8')
        plt.title('后验分布')
        plt.xlabel('正面概率 p')
        plt.ylabel('密度')
        plt.legend()
        plt.grid(True)
        
        # 子图3: 先验vs后验
        plt.subplot(2, 3, 3)
        x = np.linspace(0, 1, 100)
        prior = dist.Beta(1.0, 1.0)
        posterior = dist.Beta(alpha, beta)
        
        plt.plot(x, prior.log_prob(torch.tensor(x)).exp().numpy(), 
                label='先验 Beta(1,1)', alpha=0.7)
        plt.plot(x, posterior.log_prob(torch.tensor(x)).exp().numpy(), 
                label=f'后验 Beta({alpha:.1f},{beta:.1f})', alpha=0.7)
        plt.title('先验 vs 后验分布')
        plt.xlabel('正面概率 p')
        plt.ylabel('密度')
        plt.legend()
        plt.grid(True)
        
        # 子图4: 参数收敛
        plt.subplot(2, 3, 4)
        plt.scatter(alpha, beta, s=100, c='red', marker='o')
        plt.xlabel('Alpha参数')
        plt.ylabel('Beta参数')
        plt.title('学习到的参数')
        plt.grid(True)
        
        # 子图5: 置信区间
        plt.subplot(2, 3, 5)
        credible_interval = torch.quantile(samples, torch.tensor([0.025, 0.975]))
        plt.bar(['95%置信区间'], [credible_interval[1] - credible_interval[0]], 
               bottom=credible_interval[0], color='lightblue', alpha=0.7)
        plt.axhline(0.8, color='red', linestyle='--', label='经验概率')
        plt.ylabel('正面概率')
        plt.title('95%置信区间')
        plt.legend()
        plt.grid(True)
        
        # 子图6: 预测分布
        plt.subplot(2, 3, 6)
        posterior = dist.Beta(alpha, beta)
        p_samples = posterior.sample((1000,))
        future_tosses = dist.Bernoulli(p_samples).sample((10,)).t()
        heads_counts = future_tosses.sum(dim=1)
        
        plt.hist(heads_counts.numpy(), bins=11, alpha=0.7, color='orange')
        plt.title('未来10次投掷的正面次数分布')
        plt.xlabel('正面次数')
        plt.ylabel('频次')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('coin_bias_analysis.png', dpi=300, bbox_inches='tight')
        print("结果图表已保存为 'coin_bias_analysis.png'")
        
    except ImportError:
        print("matplotlib未安装，跳过图表绘制")


if __name__ == "__main__":
    # 运行基本推断
    alpha, beta, losses = run_basic_inference()
    
    # 高级分析
    samples, credible_interval = advanced_analysis(alpha, beta)
    
    # 比较不同先验
    prior_comparison = compare_priors()
    
    # 预测分析
    simulate_predictions(alpha, beta)
    
    # 绘制结果
    plot_results(alpha, beta, samples, losses)
    
    print("\n=== 硬币偏置学习完成 ===") 