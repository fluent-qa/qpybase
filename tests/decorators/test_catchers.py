from qpybase.decorators.wrappers import wrap_error


class AnotherError(RuntimeError):
    pass


@wrap_error(raises=AnotherError)
def raise_io_error():
    raise ValueError('should wrap this error')


def test_wrap_error():
    try:
        raise_io_error()
    except AnotherError as e:
        assert e is not None
