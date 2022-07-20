"""Top-level package for index_calculator."""

__author__ = """Ludwig Lierhammer"""
__email__ = "ludwig.lierhammer@hereon.de"
__version__ = "0.3.1"

from ._data import netcdf as test_netcdf  # noqa
from ._outputwriter import OutputWriter as outputwriter  # noqa
from ._postprocessing import PostProcessing as postprocessing  # noqa
from ._preprocessing import PreProcessing as preprocessing  # noqa
from ._processing import Processing as processing  # noqa
from ._tables import ijson  # noqa
from ._tables import pjson  # noqa
from ._tables import vjson  # noqa
from ._tables import xjson  # noqa
from .index_calculator import IndexCalculator as index_calculator  # noqa
