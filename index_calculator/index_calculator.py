"""Main module."""

from ._outputwriter import OutputWriter as outputwriter
from ._postprocessing import PostProcessing as postprocessing
from ._preprocessing import PreProcessing as preprocessing
from ._processing import Processing as processing


class IndexCalculator:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def compute(self, write=False):
        preproc_obj = preprocessing(**self.kwargs)
        proc_obj = processing(preproc_obj=preproc_obj, **self.kwargs)
        postproc_obj = postprocessing(proc_obj=proc_obj, **self.kwargs)
        if write is True:
            outputwriter(postproc_obj=postproc_obj).write_to_netcdf()
        return postproc_obj.postproc
