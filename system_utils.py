import os
from pathlib import Path


def get_init_path():
    return str(Path(os.path.realpath(__file__)).parent.absolute())