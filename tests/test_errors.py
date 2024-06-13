from rich import print

from qpybase.errors import GeneralError


def test_generic_error():
    e = GeneralError()
    e.log()
    print(e.message)
