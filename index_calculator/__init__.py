"""Top-level package for index_calculator."""

__author__ = """Ludwig Lierhammer"""
__email__ = "ludwig.lierhammer@dwd.de"

from ._outputwriter import OutputWriter as outputwriter
from ._postprocessing import PostProcessing as postprocessing
from ._preprocessing import PreProcessing as preprocessing
from ._processing import Processing as processing
from ._tables import cfjson  # noqa
from ._tables import fjson  # noqa
from ._tables import mjson  # noqa
from ._tables import pjson  # noqa
from ._tables import vjson  # noqa
from ._tables import xjson  # noqa
from .index_calculator import IndexCalculator as index_calculator


def _get_version():
    __version__ = "unknown"
    try:
        from ._version import __version__
    except ImportError:
        pass
    return __version__


__version__ = _get_version()

preprocessing.__module__ = __name__
preprocessing.__name__ = "preprocessing"
processing.__module__ = __name__
processing.__name__ = "processing"
postprocessing.__module__ = __name__
postprocessing.__name__ = "postprocessing"
outputwriter.__module__ = __name__
outputwriter.__name__ = "outputwriter"
index_calculator.__module__ = __name__
index_calculator.__name__ = "index_calculator"
