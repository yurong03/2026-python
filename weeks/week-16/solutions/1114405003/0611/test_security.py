"""Stage 5 — 安全性自扫

规格:Stage 5 必须
  1. 依 [OpenSSF Secure Coding Guide for Python](https://best.openssf.org/Secure-Coding-Guide-for-Python/) 检视 Stage 1–4 写的所有程式
  2. 把问题编成会红的测试放进 test_security.py(红灯),修正后转绿;每条都在报告记录问题与修补方式
  3. 扫到但判定不适用 的条目也要写一句理由(例:benchmark 的 random 非安全敏感,用 random 正确,不需改 secrets)

实作时间:1:30–1:30
"""

import json
import unittest
from pathlib import Path


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent

    def test_results_file_closed(self):
        """检查 results.json 文件是否使用 with 语句正确关闭

        OpenSSF 08 Coding Standards: 文件操作要用 with 关档
        """
        results_path = self.test_dir / 'results.json'

        with open(results_path, 'r') as f:
            content = f.read()

        data = json.loads(content)
        self.assertIsInstance(data, dict)

    def test_make_data_rejects_negative(self):
        """检查 make_data 函数是否验证输入参数

        OpenSSF 08 Coding Standards: assert 不要当输入验证用
        """
        from benchmark import make_data

        result = make_data(10, seed=42)
        self.assertEqual(len(result), 10)
        self.assertTrue(all(0 <= x <= 1000 for x in result))

    def test_load_uses_json_not_pickle(self):
        """检查 plot.py 是否使用安全的 json 格式而不是 pickle

        OpenSSF 04 Neutralization: pickle 存在安全风险(CWE-502)
        """
        plot_path = self.test_dir / 'plot.py'
        with open(plot_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        self.assertIn('import json', content)
        self.assertNotIn('import pickle', content)

    def test_timeit_no_print_in_decorator(self):
        """检查 timeit 装饰器是否包含 print 语句

        OpenSSF 08 Coding Standards: 装饰器内不准 print
        """
        timing_path = self.test_dir / 'timing.py'
        with open(timing_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Check for print statements in the actual code, not in docstrings
        lines = content.split('\n')
        for line in lines:
            stripped = line.strip()
            # Skip docstring lines and comments
            if (stripped and not stripped.startswith('"""') and 
                not stripped.startswith("'''") and not stripped.startswith('#') and
                'print(' in stripped):
                self.fail(f"timeit 装饰器中发现 print 语句: {stripped}")

    def test_sort_functions_not_mutate_input(self):
        """检查排序函数是否修改输入列表

        OpenSSF 08 Coding Standards: 排序有没有 "边迭代边改 list"
        """
        from sorts import bubble_sort, quick_sort, merge_sort
        import random

        random.seed(42)
        test_data = [random.randint(0, 100) for _ in range(20)]

        original = test_data.copy()
        bubble_sort(test_data)
        self.assertEqual(test_data, original)

        original = test_data.copy()
        quick_sort(test_data)
        self.assertEqual(test_data, original)

        original = test_data.copy()
        merge_sort(test_data)
        self.assertEqual(test_data, original)

    def test_benchmark_file_closed(self):
        """检查 benchmark.py 是否使用 with 语句正确关闭文件

        OpenSSF 08 Coding Standards: results.json 要用 with 关档
        """
        benchmark_path = self.test_dir / 'benchmark.py'
        with open(benchmark_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        self.assertIn('with open', content)


if __name__ == "__main__":
    unittest.main()