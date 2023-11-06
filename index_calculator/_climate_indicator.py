from copy import deepcopy
from inspect import signature
from warnings import warn

import dask
import xarray as xr
from xclim.core.calendar import percentile_doy
from xclim.core.units import convert_units_to

from ._consts import _base_period as BASE_PERIOD


class ClimateIndicator:
    def __init__(self):
        self.func = None
        self.units = {}
        self.date_bounds = None
        self.base_period_time_range = BASE_PERIOD
        self.split_large_chunks = True

    def _thresh_string(self, thresh, units):
        if isinstance(thresh, str):
            return thresh
        else:
            return f"{str(thresh)} {units}"

    def _get_da(self, dictionary, var):
        if "ds" in dictionary.keys():
            return dictionary["ds"][var]
        elif var in dictionary.keys():
            return dictionary[var]
        raise ValueError("Variable {} not found!")

    def _clean_up_params(self, params, func, exceptions=[]):
        del_list = []
        if not callable(func):
            return params
        for param in params.keys():
            if param in exceptions:
                continue
            if param not in signature(func).parameters.keys():
                warn(
                    f"Function {func} does not provide parameter {param}\n"
                    "The parameter will be deleted \n"
                    "from parameter list"
                )
                del_list.append(param)
        for param in del_list:
            del params[param]
        return params

    def _set_default_if_None(self, params):
        params_ = {}
        for k, v in params.items():
            if isinstance(v, dict):
                v = self._set_default_if_None(v)
            if v is None:
                if hasattr(self, k):
                    v = getattr(self, k)
                else:
                    continue
            params_[k] = v
        return params_

    def _add_units(self, params):
        params_ = {}
        for k, v in params.items():
            if isinstance(v, dict):
                v = self._add_units(v)
            if k in self.units.keys():
                v = self._thresh_string(v, self.units[k])
            params_[k] = v
        return params_

    def _dates_to_bounds(self, kwargs):
        kwargs["date_bounds"] = (kwargs["start_date"], kwargs["end_date"])
        return kwargs

    def _filter_out_small_values(self, da, thresh="1mm/day", context="hydro"):
        thresh = convert_units_to(thresh, da, context=context)
        return da.where(da > thresh)

    def _get_percentile(self, da, per, base_period_time_range):
        if isinstance(per, xr.Dataset):
            return per["per"]
        elif isinstance(per, xr.DataArray):
            return per
        tslice = slice(base_period_time_range[0], base_period_time_range[1])
        base_period = da.sel(time=tslice)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            per_doy = percentile_doy(base_period, per=per)
            per_doy_comp = per_doy.compute()
        return per_doy_comp.sel(percentiles=per)

    def _preprocessing(self, da, method=None, **kwargs):
        kwargs_ = deepcopy(kwargs)
        kwargs = self._clean_up_params(
            params=kwargs_, func=self._filter_out_small_values
        )
        if method == "precipitation":
            da = self._filter_out_small_values(da, **kwargs)
        return da

    def _get_percentiles(self, params, kwargs):
        self.split_large_chunks = False
        for name_per, kwargs_dict in kwargs["percentiles"].items():
            if name_per in kwargs.keys():
                if isinstance(kwargs[name_per], (xr.DataArray, xr.Dataset)):
                    continue
            da = self._get_da(params, kwargs_dict["variable"])
            da = self._preprocessing(
                da,
                method=kwargs_dict["method"],
                **kwargs,
            )
            kwargs[name_per] = self._get_percentile(
                da, kwargs_dict["per"], kwargs["base_period_time_range"]
            )
        return kwargs

    def compute_climate_indicator(self, params, **kwargs):
        params = self._clean_up_params(params=params, func=self.func)
        kwargs = self._set_default_if_None(kwargs)
        kwargs = self._add_units(kwargs)
        if "percentiles" in kwargs.keys():
            kwargs = self._get_percentiles(params, kwargs)
        if self.date_bounds is True:
            kwargs = self._dates_to_bounds(kwargs)
        if self.func is None:
            return kwargs
        kwargs = self._clean_up_params(
            params=kwargs, func=self.func, exceptions=["date_bounds"]
        )
        if self.split_large_chunks is True:
            return self.func(**params, **kwargs)
        if self.split_large_chunks is False:
            with dask.config.set(
                **{
                    "array.slicing.split_large_chunks": False,
                }
            ):
                return self.func(**params, **kwargs)
