"""Stage 4 — 实验结果图表与报告

规格:plot.py 必须
  1. 实现 load_results(path: str) -> dict
  2. 实现 plot_results(results: dict, out_path: str) -> None
  3. 折线图:x 轴 = 数据量 n,y 轴 = 平均秒数(**y 轴用 log scale**,不然 O(n²) 会把其他线压扁)
  4. 每个算法一条线(含 baseline 与加速版),输出 `assets/benchmark.png`
  5. 测试需验证 PNG 确实产生且非空档;环境限制:`plot.py` 开头加 `matplotlib.use("Agg")` 才能在无窗环境跑

实现时间:1:15–1:30
"""

import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_results(path: str) -> dict:
    """从 JSON 文件加载排序 benchmark 结果

    Args:
        path: results.json 文件的路径

    Returns:
        包含排序性能数据的字典
    """
    with open(path, 'r') as f:
        return json.load(f)


def plot_results(results: dict, out_path: str) -> None:
    """绘制排序性能比较图表

    Args:
        results: 包含排序性能数据的字典
        out_path: 输出图表的路径
    """
    plt.figure(figsize=(12, 8))

    # Collect data for each algorithm across all sizes
    algorithm_data = {}
    for size, algorithms in results.items():
        n = int(size)
        for name, metrics in algorithms.items():
            if name not in algorithm_data:
                algorithm_data[name] = {'x': [], 'y': []}
            algorithm_data[name]['x'].append(n)
            algorithm_data[name]['y'].append(metrics['avg_time'])

    # Plot each algorithm as a single line
    for name, data in algorithm_data.items():
        # Sort by x to ensure lines connect properly
        sorted_pairs = sorted(zip(data['x'], data['y']))
        x_sorted = [p[0] for p in sorted_pairs]
        y_sorted = [p[1] for p in sorted_pairs]
        plt.plot(x_sorted, y_sorted, 'o-', label=name, linewidth=2, markersize=8)

    plt.yscale('log')
    plt.xlabel('数据量 (n)', fontsize=12)
    plt.ylabel('平均时间 (秒, log scale)', fontsize=12)
    plt.title('排序算法性能比较', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    results = load_results('results.json')
    plot_results(results, 'assets/benchmark.png')
    print(f"图表已保存到 assets/benchmark.png")