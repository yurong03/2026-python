"""Stage 3 — 排序加速實驗

規格:Stage 3 必須
  1. 把內建 sorted() 加入 benchmark 當 baseline
  2. 至少一種加速方案(Cython 或演算法優化)
  3. 加速版必須通過 Stage 2 同一組正確性測試
  4. 加速前後的數據都要進 results.json,報告要寫出加速比

實作時間:1:00–1:15
"""

import json
import random
from timing import timeit


def make_data(n: int, seed: int = 42) -> list:
    """生成指定長度的隨機整數列表

    Args:
        n: 列表長度
        seed: 隨機種子，用於重現實驗

    Returns:
        包含 n 個隨機整數的列表
    """
    random.seed(seed)
    return [random.randint(0, 1000) for _ in range(n)]


@timeit
def _benchmark_sort(sort_func, data):
    """對指定的排序函式進行一次測量

    Args:
        sort_func: 排序函式
        data: 要排序的數據

    Returns:
        排序後的結果
    """
    return sort_func(data)


def run_benchmark(sizes=(500, 1000, 2000, 4000), repeats=3) -> dict:
    """運行排序演算法的效能比較，包括 baseline 和加速版

    Args:
        sizes: 要測試的數據規模列表
        repeats: 每種規模的重複次數

    Returns:
        包含每種排序在每種規模下的效能數據的字典
    """
    results = {}
    sort_functions = {
        'bubble_sort': bubble_sort,
        'quick_sort': quick_sort,
        'merge_sort': merge_sort,
        'sorted()': sorted,
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


# Stage 2 排序函式

def bubble_sort(data):
    """優化版冒泡排序實現

    Args:
        data: 要排序的整數列表

    Returns:
        排序後的新列表
    """
    result = data.copy()
    n = len(result)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


def quick_sort(data):
    """優化版快速排序實現(Median-of-three pivot)

    Args:
        data: 要排序的整數列表

    Returns:
        排序後的新列表
    """
    result = data.copy()

    def _quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            _quick_sort(arr, low, pi - 1)
            _quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        mid = (low + high) // 2
        pivot_candidates = [arr[low], arr[mid], arr[high]]
        pivot_candidates.sort()
        pivot = pivot_candidates[1]

        if pivot == arr[low]:
            pivot_index = low
        elif pivot == arr[mid]:
            pivot_index = mid
        else:
            pivot_index = high

        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _quick_sort(result, 0, len(result) - 1)
    return result


def merge_sort(data):
    """優化版合併排序實現(對小陣列使用插入排序)

    Args:
        data: 要排序的整數列表

    Returns:
        排序後的新列表
    """
    result = data.copy()

    def insertion_sort(arr, start, end):
        for i in range(start + 1, end + 1):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key

    def _merge_sort(arr, start, end):
        if end - start + 1 <= 16:
            insertion_sort(arr, start, end)
            return

        mid = (start + end) // 2
        _merge_sort(arr, start, mid)
        _merge_sort(arr, mid + 1, end)

        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    _merge_sort(result, 0, len(result) - 1)
    return result


if __name__ == "__main__":
    results = run_benchmark()

    print("\n排序效能比較表(包含 baseline 和加速版)")
    print("=" * 70)
    print(f"{'規模':<8} {'排序演算法':<15} {'平均時間(秒)':<15} {'最小時間(秒)':<15} {'最大時間(秒)':<15}")
    print("-" * 70)

    for size, data in results.items():
        for name, metrics in data.items():
            print(f"{size:<8} {name:<15} {metrics['avg_time']:<15.6f} "
                  f"{metrics['min_time']:<15.6f} {metrics['max_time']:<15.6f}")

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n結果已保存到 results.json")
