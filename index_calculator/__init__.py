"""Top-level package for index_calculator."""

__author__ = """Ludwig Lierhammer"""
__email__ = "ludwig.lierhammer@hereon.de"
__version__ = "0.1.0"

from ._outputwriter import OutputWriter as outputwriter  # noqa
from ._postprocessing import PostProcessing as postprocessing  # noqa
from ._preprocessing import PreProcessing as preprocessing  # noqa
from ._processing import Processing as processing  # noqa
from .index_calculator import IndexCalculator as index_calculator  # noqa
