import cftime
import pyhomogenize as pyh
import xarray as xr

from ._consts import _tfreq
from ._indices import ClimateIndices as ci
from ._utils import check_existance, kwargs_to_self, object_attrs_to_self


class Processing:
    """Class for proecssing."""

    def __init__(
        self,
        index=None,
        preproc_obj=None,
        **kwargs,
    ):
        """Write parameters to self."""
        if preproc_obj is None:
            raise ValueError(
                "Please select an index_calculator.PreProcessing object."
                "'preproc_obj='...'"
            )
        object_attrs_to_self(preproc_obj, self)

        self.CIname = check_existance({"index": index}, self)
        kwargs_to_self(kwargs, self)
        self.proc = self.processing()

    def processing(self):
        """Calculate climate index."""
        array = getattr(ci(), self.CIname)(self.preproc, self.freq)
        basics = pyh.basics()
        date_range = basics.date_range(
            start=self.preproc.time.values[0],
            end=self.preproc.time.values[-1],
            frequency=_tfreq[self.freq],
        )
        array = array.assign_coords({"time": date_range})
        data_vars = {
            k: self.preproc.data_vars[k]
            for k in self.preproc.data_vars.keys()
            if k not in self.var_name
        }
        data_vars[self.CIname] = array
        data_vars["time"] = array["time"]
        del data_vars["time_bnds"]
        idx_ds = xr.Dataset(data_vars=data_vars, attrs=self.preproc.attrs)
        new_time = cftime.date2num(
            idx_ds.time,
            self.ds.time.encoding["units"],
            calendar=self.ds.time.encoding["calendar"],
        )
        idx_ds = idx_ds.assign_coords({"time": new_time})
        idx_ds = idx_ds.cf.add_bounds("time")
        idx_ds = idx_ds.reset_coords("time_bounds")
        idx_ds["time_bounds"] = idx_ds.time_bounds.transpose()

        new_time = cftime.num2date(
            idx_ds.time,
            self.ds.time.encoding["units"],
            calendar=self.ds.time.encoding["calendar"],
        )
        new_time_bnds = cftime.num2date(
            idx_ds.time_bounds,
            self.ds.time.encoding["units"],
            calendar=self.ds.time.encoding["calendar"],
        )
        idx_ds = idx_ds.assign_coords({"time": new_time})
        idx_ds.time_bounds.values = new_time_bnds
        return idx_ds.rename({"time_bounds": "time_bnds"})
