import qpybase


def test_logger():
    qpybase.logger.info("this is info level")
    qpybase.logger.debug("this is info level")
    qpybase.logger.warning("this is info level")
    qpybase.logger.error("this is info level")
