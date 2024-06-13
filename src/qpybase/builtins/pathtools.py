import sys

from pathlib import Path


def get_project_rootpath(bin_path=".venv/bin"):
    return Path(sys.executable).parent.resolve().__str__().replace(bin_path, "")
