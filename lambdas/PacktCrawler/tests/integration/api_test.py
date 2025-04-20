# Builtin imports
import os
import sys

# 3rd-party imports
import pytest

# Local imports
sys.path.append(os.path.join(os.path.dirname(__file__), *[".."]*4, "libs"))
from src.app import lambda_handler

def test_lambda_handler():
    lambda_handler(None, None)
