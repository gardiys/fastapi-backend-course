import os
from os.path import abspath, dirname

ENV_FILE_NAME: str = ".env"
ENV_FILE_PATH: str = os.path.join(dirname(abspath(__file__)), ENV_FILE_NAME)
