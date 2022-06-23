"""Main module."""

from ._outputwriter import OutputWriter as outputwriter
from ._postprocessing import PostProcessing as postprocessing
from ._preprocessing import PreProcessing as preprocessing
from ._processing import Processing as processing


class IndexCalculator:
    """Class for calculating climate indices with xclim."""

    def __init__(self, output=True, **kwargs):
        """Write input parameters to self."""
        self.output = output
        self.kwargs = kwargs

    def compute(self, write=False):
        """Compute climate index.

        Parameters
        ----------
        write: bool, optional
           If True write climate index dataset on disk.

        Returns
        -------
        PostProcessing object
        """
        preproc_obj = preprocessing(**self.kwargs)
        proc_obj = processing(preproc_obj=preproc_obj)
        postproc_obj = postprocessing(proc_obj=proc_obj)
        if write is True:
            outputwriter(
                postproc_obj=postproc_obj,
            ).write_to_netcdf(self.output)
        return postproc_obj
