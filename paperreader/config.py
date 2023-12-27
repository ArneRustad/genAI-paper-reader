import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, os.pardir))

DIR_DATA = os.path.join(_PROJECT_DIR, "data/")
DIR_PROMPTS = os.path.join(_CURRENT_DIR, "prompts/")