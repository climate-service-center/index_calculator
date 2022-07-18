import re

import cftime
import pyhomogenize as pyh
import xarray as xr

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
        kwargs_to_self(kwargs, self)
        self._get_idx_name_and_repl()
        self.proc = self.processing()

    def _get_numb_name_and_idx_object(self):
        alpha_name = "".join(filter(lambda x: x.isalpha(), self.CIname))
        numb_name = "".join(filter(lambda x: x.isdigit(), self.CIname))
        replace_name = re.sub(r"\d+", "YY", self.CIname)
        if hasattr(indices, self.CIname):
            idx_object = getattr(indices, self.CIname)
            self.IDXname = self.CIname
            numb_name = ""
        elif hasattr(indices, alpha_name):
            idx_object = getattr(indices, alpha_name)
            self.IDXname = alpha_name
        elif hasattr(indices, replace_name):
            idx_object = getattr(indices, replace_name)
            self.IDXname = replace_name
        else:
            raise NameError("{} not defined.".format(self.CIname))
        return numb_name, idx_object

    def _get_replacement(self, obj, numb_name):
        replacement = {}
        repl_value = ""
        for attr in dir(obj):
            if attr[0] == "_":
                continue
            if callable(getattr(obj, attr)):
                continue
            if attr in self.kwargs.keys():
                replacement[attr] = self.kwargs[attr]
            elif numb_name:
                replacement[attr] = numb_name
            else:
                replacement[attr] = getattr(obj, attr)
            if repl_value == "":
                if isinstance(replacement[attr], list):
                    continue
                repl_value = replacement[attr]
                if isinstance(repl_value, str) and len(repl_value) > 0:
                    if repl_value[0] == "0":
                        repl_value = float(
                            "{}.{}".format(
                                repl_value[0],
                                repl_value[1:],
                            )
                        )
                    else:
                        repl_value = int(repl_value)
                replacement[attr] = repl_value
                repl_value = str(repl_value)
        return replacement, repl_value

    def _get_idx_name_and_repl(self):
        numb_name, idx_object = self._get_numb_name_and_idx_object()
        object_attrs_to_self(idx_object, self, overwrite=False)
        self.replacement, self.repl_value = self._get_replacement(
            idx_object,
            numb_name,
        )
        if not self.repl_value:
            pass
        elif "YY" in self.CIname:
            self.CIname = self.CIname.replace("YY", self.repl_value)
        elif numb_name:
            self.CIname = self.CIname = self.CIname.replace(
                numb_name,
                self.repl_value,
            )
        elif self.repl_value not in self.CIname:
            self.CIname = "{}{}".format(self.CIname, self.repl_value)

    def _adjust_params_to_ci(self):
        params = {
            "ds": self.preproc,
            "freq": _freq[self.freq],
        }
        params.update(self.replacement)
        return params

    def processing(self):
        """Calculate climate index."""
        params = self._adjust_params_to_ci()
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
