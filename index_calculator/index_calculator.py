"""Main module."""

from ._outputwriter import OutputWriter as outputwriter
from ._postprocessing import PostProcessing as postprocessing
from ._preprocessing import PreProcessing as preprocessing
from ._processing import Processing as processing


class IndexCalculator:
    """Class for calculating climate indices with xclim.

    Parameters
    ----------
    write: bool (default: False), optional
        If True write climate index dataset on disk.

    Notes
    -----
    For more parameter information see:

        :func:`~index_calculator.preprocessing`
        :func:`~index_calculator.processing`
        :func:`~index_calculator.postprocessing`
        :func:`~index_calculator.outputwriter`

    Example
    -------
    Calculate climate indicator and write dataset as netcdf fiel on disk::

        from pyhomogenize import open_xrdataset
        from index_calculator import index_calculator

        netcdf_file = "tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_"
                      "GERICS-REMO2015_v1_day_20010101-20051231.nc"
        ds = open_xrdataset(netcdf_file)

        idx = index_calculator(
                write=True,
                ds=ds,
                index="TG",
                project="CORDEX",
                institution_id="GERICS",
                institution="Helmholtz-Zentrum hereon GmbH,"
                            "Climate Service Center Germany",
                contact="gerics-cordex@hereon.de",
        )

        --> File written: TG_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_
                          GERICS-REMO2015_v1_day_GERICS_year_2001-2005.nc

    """

    def __init__(self, write=False, **kwargs):
        self.kwargs = kwargs
        self._compute(write)

    def _compute(self, write):
        """Compute climate index."""
        preproc_obj = preprocessing(**self.kwargs)
        proc_obj = processing(preproc_obj=preproc_obj)
        postproc_obj = postprocessing(proc_obj=proc_obj)
        if write is True:
            outputwriter(
                postproc_obj=postproc_obj,
                **self.kwargs,
            )
        return postproc_obj
