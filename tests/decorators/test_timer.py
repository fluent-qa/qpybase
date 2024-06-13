
from time import sleep

from qpybase.decorators.timer import timer, profile_timer


@timer()
@profile_timer()
def demo_function():
    sleep(1)


def test_timeit():
    demo_function()
