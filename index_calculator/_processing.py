import cftime
import pyhomogenize as pyh
import xarray as xr

# from ._indices import ClimateIndices as ci
from . import _indices as indices
from ._consts import _freq, _tfreq
from ._utils import check_existance, kwargs_to_self, object_attrs_to_self


class Processing:
    """Class for processing."""

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
        alpha_name = "".join(filter(lambda x: x.isalpha(), self.CIname))
        numb_name = "".join(filter(lambda x: x.isdigit(), self.CIname))
        if hasattr(indices, self.CIname):
            idx_object = getattr(indices, self.CIname)
            self.IDXname = self.CIname
        elif hasattr(indices, alpha_name):
            idx_object = getattr(indices, alpha_name)
            if numb_name[0] == "0":
                number = float("{}.{}".format(numb_name[0], numb_name[1:]))
            else:
                number = int(numb_name)
            kwargs["thresh"] = number
            self.IDXname = alpha_name
        else:
            raise NameError("{} not defined.".format(self.CIname))

        object_attrs_to_self(idx_object, self)
        kwargs_to_self(kwargs, self)
        self.proc = self.processing()

    def adjust_params_to_ci(self):
        params = {
            "ds": self.preproc,
            "freq": _freq[self.freq],
        }
        params.update(self.parameters)
        for key, value in self.kwargs.items():
            if key in self.parameters.keys():
                params[key] = value
        return params

    def processing(self):
        """Calculate climate index."""
        params = self.adjust_params_to_ci()
        array = self.compute(**params)
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
        encoding = {
            "units": self.ds.time.encoding["units"],
            "calendar": self.ds.time.encoding["calendar"],
            "dtype": self.ds.time.encoding["dtype"],
        }
        self.encoding = {
            "time": encoding,
        }
        if len(idx_ds.time) > 1:
            idx_ds = idx_ds.cf.add_bounds("time")
            idx_ds = idx_ds.reset_coords("time_bounds")
            idx_ds["time_bounds"] = idx_ds.time_bounds.transpose()

            new_time_bnds = cftime.num2date(
                idx_ds.time_bounds,
                self.ds.time.encoding["units"],
                calendar=self.ds.time.encoding["calendar"],
            )
            idx_ds.time_bounds.values = new_time_bnds
            idx_ds = idx_ds.rename({"time_bounds": "time_bnds"})
            self.encoding["time_bnds"] = encoding

        new_time = cftime.num2date(
            idx_ds.time,
            self.ds.time.encoding["units"],
            calendar=self.ds.time.encoding["calendar"],
        )
        idx_ds = idx_ds.assign_coords({"time": new_time})
        return idx_ds
