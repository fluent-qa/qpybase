from time import sleep

from qpybase.decorators.timer import profile_timer, timer


@timer()
@profile_timer()
def demo_function():
    sleep(1)


def test_timeit():
    demo_function()
