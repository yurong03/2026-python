"""Stage 2 — 排序效能量测

规格:benchmark.py 必须
  1. 实现 make_data(n: int, seed: int = 42) -> list
  2. 实现 run_benchmark(sizes=(500, 1000, 2000, 4000), repeats=3) -> dict
  3. 用 timeit 测量，每个 n 重复 repeats 次取 records 平均
  4. python benchmark.py 打印比较表，并把结果存成 results.json

实现时间:0:40–1:00
"""

import json
import random
from timing import timeit
from sorts import bubble_sort, quick_sort, merge_sort


def make_data(n: int, seed: int = 42) -> list:
    """生成指定长度的随机整数列表

    Args:
        n: 列表长度
        seed: 随机种子，用于重现实验

    Returns:
        包含 n 个随机整数的列表
    """
    random.seed(seed)
    return [random.randint(0, 1000) for _ in range(n)]


@timeit
def _benchmark_sort(sort_func, data):
    """对指定的排序函数进行一次测量

    Args:
        sort_func: 排序函数
        data: 要排序的数据

    Returns:
        排序后的结果
    """
    return sort_func(data)


def run_benchmark(sizes=(500, 1000, 2000, 4000), repeats=3) -> dict:
    """运行排序算法的性能比较

    Args:
        sizes: 要测试的数据规模列表
        repeats: 每种规模的重复次数

    Returns:
        包含每种排序在每种规模下的性能数据的字典
    """
    results = {}
    sort_functions = {
        'bubble_sort': bubble_sort,
        'quick_sort': quick_sort,
        'merge_sort': merge_sort,
    }

    for size in sizes:
        data = make_data(size)
        results[str(size)] = {}

        for name, sort_func in sort_functions.items():
            times = []

            for _ in range(repeats):
                _benchmark_sort(sort_func, data)
                times.append(_benchmark_sort.last_elapsed)

            avg_time = sum(times) / len(times)
            results[str(size)][name] = {
                'avg_time': avg_time,
                'times': times,
                'min_time': min(times),
                'max_time': max(times),
            }

    return results


if __name__ == "__main__":
    results = run_benchmark()

    print("\n排序效能比较表")
    print("=" * 60)
    print(f"{'规模':<8} {'排序算法':<15} {'平均时间(秒)':<15} {'最小时间(秒)':<15} {'最大时间(秒)':<15}")
    print("-" * 60)

    for size, data in results.items():
        for name, metrics in data.items():
            print(f"{size:<8} {name:<15} {metrics['avg_time']:<15.6f} "
                  f"{metrics['min_time']:<15.6f} {metrics['max_time']:<15.6f}")

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n结果已保存到 results.json")