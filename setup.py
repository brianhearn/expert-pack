"""Shim so `pip install -e .` works on older pip that requires setup.py.

All package metadata lives in pyproject.toml; setuptools reads it from there.
"""

from setuptools import setup

setup()
