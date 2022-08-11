"""Main module."""

from ._outputwriter import OutputWriter as outputwriter
from ._postprocessing import PostProcessing as postprocessing
from ._preprocessing import PreProcessing as preprocessing
from ._processing import Processing as processing
from ._utils import kwargs_to_self, object_attrs_to_self


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

        --> File written: cordex/climdex/EUR-11/GERICS/GERICS/MPI-M-MPI-ESM-LR/
                          historical/r3i1p1/GERICS-REMO2015/v1/year/TG/
                          TG_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_
                          GERICS-REMO2015_v1_day_GERICS_year_2001-2005.nc

    """

    def __init__(self, write=False, **kwargs):
        kwargs_to_self(kwargs, self)
        postproc_obj = self._compute(write=write, **kwargs)
        object_attrs_to_self(postproc_obj, self)

    def _compute(self, write=False, **kwargs):
        """Compute climate index."""
        preproc_obj = preprocessing(**kwargs)
        proc_obj = processing(preproc_obj=preproc_obj)
        postproc_obj = postprocessing(proc_obj=proc_obj)
        if write is True:
            outputwriter(
                postproc_obj=postproc_obj,
                **kwargs,
            )
        return postproc_obj
