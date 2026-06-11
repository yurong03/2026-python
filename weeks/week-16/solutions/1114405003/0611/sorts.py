"""Stage 2 — 三種排序實作

規格:sorts.py 的 bubble_sort / quick_sort / merge_sort 必須
  1. 回傳新的排序後 list,不可修改傳入的 list
  2. 禁用內建 sorted() / list.sort()(那是 Stage 3 的對照組;
     測試裡拿 sorted() 當驗證標準則可以)

實作時間:0:15–0:40
"""

from typing import List


def bubble_sort(data: List[int]) -> List[int]:
    """冒泡排序實現

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


def quick_sort(data: List[int]) -> List[int]:
    """快速排序實現

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
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _quick_sort(result, 0, len(result) - 1)
    return result


def merge_sort(data: List[int]) -> List[int]:
    """合併排序實現

    Args:
        data: 要排序的整數列表

    Returns:
        排序後的新列表
    """
    result = data.copy()

    if len(result) <= 1:
        return result

    mid = len(result) // 2
    left = merge_sort(result[:mid])
    right = merge_sort(result[mid:])

    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """合併兩個已排序的列表

    Args:
        left: 已排序的左半部分
        right: 已排序的右半部分

    Returns:
        合併後的排序列表
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result
