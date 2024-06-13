from qpybase import settings


def test_configuration_loaded():
    print(settings)
    assert settings.log_level == "INFO"
    # configs.structure.test = "http://localhost:7077"
    # assert configs.mitm.recorded_url == "https://matrix-api,"
