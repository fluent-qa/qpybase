from typing import Callable
from typing import Tuple

import os
import subprocess
import sys

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import wait
from functools import partial
from multiprocessing import pool


def multi_thread_submit(
    func,
    items,
    max_workers=10,
):
    executor = ThreadPoolExecutor(max_workers=max_workers)
    future_list = []
    for item in items:
        future_list.append(
            executor.submit(func, *item["args"], **item["kwargs"])
        )  # .add_done_callback()
    done_iter = as_completed(future_list)
    executor.shutdown(wait=True)
    return done_iter


def multi_process_submit(
    func,
    items,
    max_workers=10,
):
    executor = ProcessPoolExecutor(max_workers=max_workers)

    future_list = []
    for item in items:
        future_list.append(
            executor.submit(func, *item["args"], **item["kwargs"])
        )  # .add_done_callback()
    done_iter = as_completed(future_list)
    executor.shutdown(wait=True)
    return done_iter


def run_threaded(fns_args: list[(Callable, Tuple)], max_threads=None):
    """
    Run a list of tasks concurrently, and return their results as
    a list in the same order. A task is a 2-tuple of the function and an
    n-tuple of the function's n arguments.
    Remember: A 1-tuple needs a trailing comma, eg. (x,)
    Return: A list of results, in the order of the input tasks.
    """
    if max_threads is None:
        max_threads = len(fns_args)
    results = []
    with ThreadPoolExecutor(max_threads) as pool:
        for fn, args in fns_args:
            future = pool.submit(fn, *args)
            results.append(future)
    wait(results)
    return [r.result() for r in results]


def run(
    command,
    input=None,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    timeout=None,
    copy_local_env=False,
    **kwargs,
):
    """
    Cross platform compatible subprocess with CompletedProcess return.

    No formatting or encoding is performed on the output of subprocess, so it's
    output will appear the same on each version / interpreter as before.

    .. code:: python

        reusables.run('echo "hello world!', shell=True)
        # CPython 3.6
        # CompletedProcess(args='echo "hello world!', returncode=0,
        #                  stdout=b'"hello world!\\r\\n', stderr=b'')
        #
        # PyPy 5.4 (Python 2.7.10)
        # CompletedProcess(args='echo "hello world!', returncode=0L,
        # stdout='"hello world!\\r\\n')

    Timeout is only usable in Python 3.X, as it was not implemented before then,
    a NotImplementedError will be raised if specified on 2.x version of Python.

    :param command: command to run, str if shell=True otherwise must be list
    :param input: send something `communicate`
    :param stdout: PIPE or None
    :param stderr: PIPE or None
    :param timeout: max time to wait for command to complete
    :param copy_local_env: Use all current ENV vars in the subprocess as well
    :param kwargs: additional arguments to pass to Popen
    :return: CompletedProcess class
    """
    if copy_local_env:
        # Copy local env first and overwrite with anything manually specified
        env = os.environ.copy()
        env.update(kwargs.get("env", {}))
    else:
        env = kwargs.get("env")

    if sys.version_info >= (3, 5):
        return subprocess.run(
            command,
            input=input,
            stdout=stdout,
            stderr=stderr,
            timeout=timeout,
            env=env,
            **kwargs,
        )

    # Created here instead of root level as it should never need to be
    # manually created or referenced
    class CompletedProcess(object):
        """A backwards compatible near clone of subprocess.CompletedProcess"""

        def __init__(self, args, returncode, stdout=None, stderr=None):
            self.args = args
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

        def __repr__(self):
            args = [
                "args={0!r}".format(self.args),
                "returncode={0!r}".format(self.returncode),
                "stdout={0!r}".format(self.stdout) if self.stdout else "",
                "stderr={0!r}".format(self.stderr) if self.stderr else "",
            ]
            return "{0}({1})".format(type(self).__name__, ", ".join(filter(None, args)))

        def check_returncode(self):
            if self.returncode:
                raise subprocess.CalledProcessError(
                    self.returncode, self.args, self.stdout
                )

    proc = subprocess.Popen(command, stdout=stdout, stderr=stderr, env=env, **kwargs)
    out, err = proc.communicate(input=input, timeout=timeout)
    return CompletedProcess(command, proc.returncode, out, err)


def run_in_pool(
    target, iterable, threaded=True, processes=4, asynchronous=False, target_kwargs=None
):
    """Run a set of iterables to a function in a Threaded or MP Pool.

    .. code: python

        def func(a):
            return a + a

        reusables.run_in_pool(func, [1,2,3,4,5])
        # [1, 4, 9, 16, 25]


    :param target: function to run
    :param iterable: positional arg to pass to function
    :param threaded: Threaded if True multiprocessed if False
    :param processes: Number of workers
    :param asynchronous: will do map_async if True
    :param target_kwargs: Keyword arguments to set on the function as a partial
    :return: pool results
    """
    my_pool = pool.ThreadPool if threaded else pool.Pool

    if target_kwargs:
        target = partial(target, **target_kwargs if target_kwargs else None)

    p = my_pool(processes)
    try:
        results = (
            p.map_async(target, iterable) if asynchronous else p.map(target, iterable)
        )
    finally:
        p.close()
        p.join()
    return results
