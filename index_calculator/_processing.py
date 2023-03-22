import cf_xarray  # noqa
import cftime  # noqa
import numpy as np
import pyhomogenize as pyh
import xarray as xr
from pyhomogenize._consts import freqs as _freq
from pyhomogenize._consts import frequencies as _tfreq

from . import _indices as indices
from ._utils import (
    check_existance,
    get_alpha_name,
    get_numb_name,
    get_replace_name,
    kwargs_to_self,
    object_attrs_to_self,
)


class Processing:
    """Class for processing ``index_calculator.preprocessing`` object.

    Parameters
    ----------
    index: str
        Climate indicator name to be calculated.
    preproc_obj: index_calculator.preprocessing
        ``index_calculator.preprocessing`` object

    Example
    -------
    Calculate a climate indicator `TG` from netcdf file on disk::

        from pyhomogenize import open_xrdataset
        from index_calculator import preprocessing
        from index_calculator import processing

        netcdf_file = "tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_"
                      "GERICS-REMO2015_v1_day_20010101-20051231.nc"
        ds = open_xrdataset(netcdf_file)

        preproc = preprocessing(ds)
        proc = processing(index="TG", preproc_obj=preproc)

        proc_ds = proc.proc
    """

    def __init__(
        self,
        index=None,
        preproc_obj=None,
        **kwargs,
    ):
        if preproc_obj is None:
            raise ValueError(
                "Please select an index_calculator.PreProcessing object."
                "'preproc_obj='...'"
            )
        object_attrs_to_self(preproc_obj, self)
        self.CIname = check_existance({"index": index}, self)
        kwargs_to_self(kwargs, self)
        self._get_idx_name_and_repl()
        self.proc = self._processing()

    def _get_numb_name_and_idx_object(self):
        alpha_name = get_alpha_name(self.CIname)
        numb_name = get_numb_name(self.CIname)
        replace_name = get_replace_name(self.CIname)
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
        for attr in dir(obj):
            if attr[0] == "_":
                continue
            if callable(getattr(obj, attr)):
                continue
            if attr in self.kwargs.keys():
                replacement[attr] = self.kwargs[attr]
            elif numb_name:
                default_value = getattr(obj, attr)
                if not isinstance(default_value, list):
                    default_value = int(default_value)
                    if default_value < 0:
                        numb_name = "-{}".format(numb_name)
                else:
                    continue
                replacement[attr] = numb_name
            else:
                replacement[attr] = getattr(obj, attr)
            if isinstance(replacement[attr], list):
                continue
            if isinstance(replacement[attr], str):
                if replacement[attr][0] == "0":
                    replacement[attr] = float(
                        "{}.{}".format(
                            replacement[attr][0],
                            replacement[attr][1:],
                        )
                    )
                else:
                    replacement[attr] = int(replacement[attr])
        return replacement

    def _get_idx_name_and_repl(self):
        numb_name, idx_object = self._get_numb_name_and_idx_object()
        defaults = [attr for attr in dir(idx_object)]
        object_attrs_to_self(idx_object, self, overwrite=False)
        self.replacement = self._get_replacement(
            idx_object,
            numb_name,
        )
        for k, v in self.replacement.items():
            if k in defaults and k in self.kwargs.keys():
                if "YY" in self.CIname:
                    self.CIname = self.CIname.replace("YY", str(v))
                elif numb_name:
                    self.CIname = self.CIname.replace(
                        numb_name,
                        v,
                    )
                elif str(v) not in self.CIname:
                    self.CIname = "{}{}".format(self.CIname, str(v))
                break

    def _adjust_params_to_ci(self):
        params = {
            "ds": self.preproc,
            "freq": _freq[self.freq],
        }
        params.update(self.replacement)
        return params

    def _processing(self):
        """Calculate climate index."""
        dvars = self.preproc.data_vars
        params = self._adjust_params_to_ci()
        array = self.compute(**params)
        basics = pyh.basics()
        data_vars = {
            k: v
            for k, v in dvars.items()
            if k not in self.var_name and "time" not in self.ds[k].coords
        }
        if "grid_mapping" in self.ds[self.var_name[0]].attrs:
            gm = self.ds[self.var_name[0]].attrs["grid_mapping"]
            array.attrs["grid_mapping"] = gm
        coords = {k: v for k, v in self.ds.coords.items() if "time" not in k}
        for k, v in coords.items():
            array[k] = v

        data_vars[self.CIname] = array
        idx_ds = xr.Dataset(
            data_vars=data_vars,
            coords=coords,
            attrs=self.preproc.attrs,
        )
        if "time" in array.coords:
            date_range = basics.date_range(
                start=self.preproc.time.values[0],
                end=self.preproc.time.values[-1],
                frequency=_tfreq[self.freq],
            )
            idx_ds = idx_ds.assign_coords(
                {"time": date_range},
            )
            idx_ds = idx_ds.squeeze()
            time_encoding = self.ds.time.encoding
            time_encoding["dtype"] = np.float64
            idx_ds.time.encoding = time_encoding
            idx_ds = (
                pyh.time_control(idx_ds)
                .add_time_bounds(
                    frequency=self.freq,
                )
                .ds
            )
            self.unlimited_dims = "time"
        else:
            for dim in idx_ds[self.CIname].dims:
                if dim not in self.preproc[self.var_name[0]].dims:
                    self.unlimited_dims = dim
                    break
            idx_ds[self.unlimited_dims] = idx_ds[self.unlimited_dims].astype(
                float,
            )
            transpose_list = list(
                map(
                    lambda x: x.replace("time", self.unlimited_dims),
                    self.preproc[self.var_name[0]].dims,
                ),
            )
            idx_ds[self.CIname] = idx_ds[self.CIname].transpose(
                *transpose_list,
            )

        for data_var in idx_ds.data_vars:
            data_var_repl = data_var.replace("bounds", "bnds")
            idx_ds = idx_ds.rename({data_var: data_var_repl})
        return idx_ds
