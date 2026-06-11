"""Stage 4 — 繪圖輸出測試

規格:plot.py 的 load_results / plot_results 必須
  1. load_results(path) 能正確讀 results.json
  2. plot_results(results, out_path) 輸出 assets/benchmark.png
  3. PNG 檔確實產生且非空檔;plot.py 開頭加 matplotlib.use("Agg")

實作時間:1:15–1:30
"""

import unittest
import os
from pathlib import Path

from plot import load_results, plot_results


class TestPlotFunctions(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(__file__).parent
        self.results_path = self.test_dir / 'results.json'
        self.output_path = self.test_dir / 'assets' / 'benchmark.png'

    def test_load_results(self):
        results = load_results(str(self.results_path))
        self.assertIsInstance(results, dict)
        self.assertIn('500', results)
        self.assertIn('1000', results)
        self.assertIn('2000', results)
        self.assertIn('4000', results)

        for size in ['500', '1000', '2000', '4000']:
            self.assertIn('bubble_sort', results[size])
            self.assertIn('quick_sort', results[size])
            self.assertIn('merge_sort', results[size])
            self.assertIn('sorted()', results[size])

    def test_plot_results_creates_file(self):
        results = load_results(str(self.results_path))
        plot_results(results, str(self.output_path))

        self.assertTrue(self.output_path.exists())

    def test_plot_results_file_not_empty(self):
        results = load_results(str(self.results_path))
        plot_results(results, str(self.output_path))

        file_size = self.output_path.stat().st_size
        self.assertGreater(file_size, 0)

    def test_plot_results_creates_assets_directory(self):
        results = load_results(str(self.results_path))
        plot_results(results, str(self.output_path))

        self.assertTrue(self.output_path.parent.exists())


if __name__ == "__main__":
    unittest.main()