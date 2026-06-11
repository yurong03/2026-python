"""Stage 1 — @timeit 裝飾器測試骨架

規格:timing.py 的 timeit 裝飾器必須
  1. 不改變被裝飾函式的回傳值
  2. 用 functools.wraps 保留 __name__ / __doc__
  3. 每次呼叫後更新 f.last_elapsed(float 秒)並 append 到 f.records
  4. 裝飾器內不准 print

待辦:
  1. 自己打提示詞跟 AI 討論,補齊下面三個測試(可再加)
  2. 跑 `python -m unittest` 確認全紅
  3. commit: "test: stage1 timeit 裝飾器測試"
  4. 寫 timing.py,全綠後 commit: "feat: stage1 實作 timeit 裝飾器"
"""

import unittest
from timing import timeit


class TestTimeit(unittest.TestCase):
    def test_returns_original_result(self):
        @timeit
        def add(a, b):
            return a + b

        result = add(2, 3)
        self.assertEqual(result, 5)
        self.assertEqual(add.last_elapsed, add.records[0])

    def test_preserves_function_metadata(self):
        @timeit
        def example_function():
            """This is an example function."""
            return 42

        self.assertEqual(example_function.__name__, "example_function")
        self.assertEqual(example_function.__doc__, "This is an example function.")

    def test_records_elapsed_time(self):
        @timeit
        def sleep_a_bit():
            import time
            time.sleep(0.01)
            return "done"

        result = sleep_a_bit()
        self.assertEqual(result, "done")
        self.assertGreater(sleep_a_bit.last_elapsed, 0)
        self.assertEqual(len(sleep_a_bit.records), 1)

    def test_multiple_calls_accumulate_records(self):
        @timeit
        def quick_calc(x):
            return x * 2

        quick_calc(1)
        quick_calc(2)
        quick_calc(3)

        self.assertEqual(len(quick_calc.records), 3)
        self.assertEqual(quick_calc.last_elapsed, quick_calc.records[-1])
        self.assertEqual(sum(quick_calc.records), quick_calc.records[0] + quick_calc.records[1] + quick_calc.records[2])


if __name__ == "__main__":
    unittest.main()
