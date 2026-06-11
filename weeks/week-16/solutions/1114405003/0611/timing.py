"""Stage 1 — @timeit 装饰器实现

规格:timing.py 的 timeit 装饰器必须
  1. 不改变被装饰函数的返回值
  2. 用 functools.wraps 保留 __name__ / __doc__
  3. 每次调用后更新 f.last_elapsed(float 秒)并 append 到 f.records
  4. 装饰器内不准 print

实现时间:0:00–0:15
"""

import functools
import time


def timeit(func):
    """计时装饰器，记录函数执行的时间

    Args:
        func: 要被装饰的函数

    Returns:
        装饰后的函数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        elapsed = end_time - start_time
        wrapper.last_elapsed = elapsed
        wrapper.records.append(elapsed)

        return result

    wrapper.last_elapsed = 0.0
    wrapper.records = []

    return wrapper
