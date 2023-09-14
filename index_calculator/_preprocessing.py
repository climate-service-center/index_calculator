import pyhomogenize as pyh
import xarray as xr
from pyhomogenize._consts import fmt as _fmt

from ._consts import _bounds
from ._tables import cfjson, fjson
from ._utils import check_existance, get_time_range_as_str, kwargs_to_self


class PreProcessing:
    """Class for pre-processing xarray datasets.

    Parameters
    ----------
    ds : xr.Dataset
        xarray Dataset.
    project: {"CORDEX", "CMIP5", "CMIP6", "EOBS", "ERA5", "N/A"}
        (default: "N/A), optional
        Project name
    var_name : str or list, optional
        CF variable(s) contained in `ds`.
        If None (default) `var_name` is read from `ds` with pyhomogenize.
    freq: str (default="year"), optional
        Climate indicator output frequency
    ifreq: str (default="day"), optional
        Climate indicator input frequency
    time_range: list, optional
        List of two strings representing the left and right time bounds.
        Select time slice with those limits from `ds`.
    crop_time_axis: bool, optional
        If True (default) select time slice from `ds`.
        The left and the right bounds depends on `freq`.
        For example: If `freq` is year the left bound has to be January, 1st
        and the right bound has to be the last day of December.
    check_time_axis: bool, optional
        If True (default) check the time axis on duplicated, redundant
        and/or missing time steps.

    Example
    -------
    Do some preprocessing with a netcdf file on disk::

        from pyhomogenize import open_xrdataset
        from index_calculator import preprocessing

        netcdf_file = "tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_"
                      "GERICS-REMO2015_v1_day_20010101-20051231.nc"
        ds = open_xrdataset(netcdf_file)

        preproc = preprocessing(ds)

        preproc_ds = preproc.preproc
    """

    def __init__(
        self,
        ds=None,
        project="N/A",
        var_name=None,
        freq="year",
        ifreq="day",
        time_range=None,
        crop_time_axis=True,
        check_time_axis=True,
        **kwargs,
    ):
        if ds is None:
            raise ValueError("Please select an input xarray dataset. 'ds=...'")

        self.ds = ds
        self.project = check_existance({"project": project}, self)
        self.var_name = var_name
        self.freq = freq
        self.ifreq = ifreq
        self.fmt = _fmt[freq].replace("-", "")
        self.afmt = _fmt[ifreq].replace("-", "")
        self.time_range = time_range
        self.crop_time_axis = crop_time_axis
        self.check_time_axis = check_time_axis
        kwargs_to_self(kwargs, self)
        self.preproc = self._preprocessing()

    def _rename_variable_names(self, ds):
        if self.project not in cfjson.keys():
            return ds
        var_names = cfjson[self.project]["variables"]
        units = cfjson[self.project]["units"]
        for dvar in ds.data_vars:
            if dvar in var_names.keys():
                ds = ds.rename({dvar: var_names[dvar]})
                dvar = var_names[dvar]
            if dvar in units.keys():
                ds[dvar].attrs["units"] = units[dvar]
        return ds

    def _convert_to_frequency(self, ds):
        if self.ifreq not in fjson.keys():
            raise ValueError(
                "Could not convert to frequency {}".format(self.ifreq),
                "Try one of {}.".format(fjson.keys()),
            )
        conv = fjson[self.ifreq]
        if conv["freq"] == xr.infer_freq(ds.time):
            return ds
        data_vars = {}
        for dvar in ds.data_vars:
            if dvar in conv["var"].keys():
                data_vars[dvar] = getattr(
                    ds[dvar].resample(time=conv["freq"]),
                    conv["var"][dvar],
                )(dim="time")
                data_vars[dvar].attrs["cell_methods"] = "time: {}".format(
                    conv["var"][dvar]
                )
                coords = data_vars[dvar].coords
        return xr.Dataset(
            data_vars=data_vars,
            coords=coords,
            attrs=ds.attrs,
        )

    def _preprocessing(self):
        ds_ = self._convert_to_frequency(self.ds)

        time_control = pyh.time_control(ds_)
        if not self.var_name:
            self.var_name = time_control.name

        avail_time = get_time_range_as_str(time_control.time, self.afmt)

        if self.time_range:
            time_control.select_time_range(self.time_range)

        if self.crop_time_axis:
            time_control.select_limited_time_range(
                smonth=_bounds[self.freq]["start"],
                emonth=_bounds[self.freq]["end"],
            )

        if self.check_time_axis:
            time_control.check_timestamps(correct=True)

        self.ATimeRange = avail_time
        ds = time_control.ds
        return self._rename_variable_names(ds)
