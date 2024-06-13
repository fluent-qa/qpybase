#!/usr/bin/env python
# -*- coding:utf-8 -*-


import contextlib
import functools
import pstats
import time

from cProfile import Profile

__all__ = ["profile_timer", "timer"]

from typing import Callable


def timer(store: bool = False, round_off: int = 10) -> Callable:
    """
    Decorator which print execution time of any function.

    Arguments:
        store: storing your execution time(store = True) or just print it (store = False).
        round_off: decimals to round off the execution time.

    Returns:
        Tuple containing return value and the execution time if store=True.
        Function's value if store=False.

    Example:

        @timer()
        def foo():
            time.sleep(1) # function sleeping for 1 second
        foo()
    """
    import time

    from functools import wraps

    def inner_timer(func: "function") -> "function":
        @wraps(func)
        def wrapper(*args: "arguments", **kwargs: "keyword arguments") -> "function":
            start_time = time.time()
            value = func(*args, **kwargs)
            finish_time = time.time()
            if store is False:
                print("=" * 100)
                print(
                    f"{func.__name__} function executed in : %s s"
                    % round((finish_time - start_time), round_off)
                )
                print("=" * 100)
                print("\n")
                return value
            else:
                exec_time = round((finish_time - start_time), round_off)
                return value, exec_time

        return wrapper

    return inner_timer


def profile_timer(sort_by="cumtime", limit=10):
    """
    :param sort_by:
    :param limit:
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrap(*args, **kwargs):
            p = Profile()
            p.enable()
            try:
                return func(*args, **kwargs)
            finally:
                p.disable()
                s = pstats.Stats(p).sort_stats(sort_by)
                s.print_stats(limit)

        return wrap

    return decorator


@contextlib.contextmanager
def prof_context(sort_by="cumtime", limit=10):
    """
    :param sort_by:
    :param limit:
    :return:
    """
    p = Profile()
    p.enable()
    try:
        yield
    finally:
        p.disable()
        s = pstats.Stats(p).sort_stats(sort_by)
        s.print_stats(limit)


# http://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p13_making_stopwatch_timer.html
class Timer:
    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError("Already started")
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError("Not started")
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
