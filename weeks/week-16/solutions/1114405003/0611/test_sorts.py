"""Stage 2 — 排序正確性測試骨架

規格:sorts.py 的 bubble_sort / quick_sort / merge_sort 必須
  1. 回傳新的排序後 list,不可修改傳入的 list
  2. 禁用內建 sorted() / list.sort()(那是 Stage 3 的對照組;
     測試裡拿 sorted() 當驗證標準則可以)

設計要求:三個函式共用同一組測試——用迴圈 + subTest,不要複製貼上三份。

待辦:
  1. 自己打提示詞跟 AI 討論,補齊測試——一般案例、edge case、
     「不可修改傳入 list」都要覆蓋;AI 給的齊不齊,自己驗收
  2. 跑 `python -m unittest` 確認全紅
  3. commit: "test: stage2 排序正確性測試"
  4. 寫 sorts.py,全綠後 commit: "feat: stage2 實作三種排序與 benchmark"
"""

import unittest
from sorts import bubble_sort, quick_sort, merge_sort
from sorts_fast import bubble_sort as bubble_sort_fast
from sorts_fast import quick_sort as quick_sort_fast
from sorts_fast import merge_sort as merge_sort_fast

# 三個排序函式都放進這個 list,每個測試用 subTest 跑一輪;
# Stage 3 的加速版 append 進來就能吃到同一組測試。
SORT_FUNCTIONS = [
    bubble_sort,
    quick_sort,
    merge_sort,
    bubble_sort_fast,
    quick_sort_fast,
    merge_sort_fast,
]


class TestSortFunctions(unittest.TestCase):
    def test_basic_cases(self):
        test_cases = [
            ([3, 1, 4, 1, 5], [1, 1, 3, 4, 5]),
            ([], []),
            ([1], [1]),
            ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
            ([2, 2, 2, 2], [2, 2, 2, 2]),
        ]

        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                for input_data, expected in test_cases:
                    result = sort_func(input_data)
                    self.assertEqual(result, expected)

    def test_random_data_matches_builtin(self):
        import random

        random.seed(42)
        test_cases = [
            [random.randint(0, 100) for _ in range(20)],
            [random.randint(-50, 50) for _ in range(30)],
            [random.randint(0, 10) for _ in range(10)],
        ]

        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                for input_data in test_cases:
                    result = sort_func(input_data)
                    expected = sorted(input_data)
                    self.assertEqual(result, expected)

    def test_input_not_mutated(self):
        import random

        random.seed(42)
        test_cases = [
            [random.randint(0, 100) for _ in range(20)],
            [random.randint(-50, 50) for _ in range(30)],
            [random.randint(0, 10) for _ in range(10)],
        ]

        for sort_func in SORT_FUNCTIONS:
            with self.subTest(sort_func=sort_func.__name__):
                for input_data in test_cases:
                    original = input_data.copy()
                    result = sort_func(input_data)
                    self.assertEqual(input_data, original, f"{sort_func.__name__} modified input list")


if __name__ == "__main__":
    unittest.main()
