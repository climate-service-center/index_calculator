import warnings
from datetime import timedelta

import xarray as xr
from pyhomogenize import basics


def object_attrs_to_self(obj, slf, overwrite=True):
    """Copy object attributes to new object."""
    for attr in dir(obj):
        if attr[0] == "_":
            continue
        if overwrite is False and hasattr(slf, attr):
            continue
        if attr[0].isalpha():
            setattr(slf, attr, getattr(obj, attr))


def kwargs_to_self(kwargs, slf):
    """Write kwargs to new object."""
    if not hasattr(slf, "kwargs"):
        setattr(slf, "kwargs", kwargs)
    else:
        slf.kwargs.update(kwargs)
    for key, value in kwargs.items():
        if not hasattr(slf, key):
            setattr(slf, key, value)
        if getattr(slf, key) is None:
            setattr(slf, key, value)


def check_existance(attr_dict, slf):
    """Check existance of values."""
    for key, value in attr_dict.items():
        test = False
        if value is None:
            method = "raise"
            test = True
        if value == "N/A":
            method = "warn"
            test = True
        if value is True:
            method = ""
            test = True
        if test:
            if hasattr(slf, key):
                return getattr(slf, key)
            else:
                msg = f"No {key} is selected. '{key}=...'"
                if method == "raise":
                    raise ValueError(msg)
                elif method == "warn":
                    warnings.warn(msg)
        return value


def get_time_range_as_str(time, fmt):
    ts = basics().date_to_str(time[0], fmt)
    te = basics().date_to_str(time[-1], fmt)
    return [ts, te]


def get_time_bounds(start, end, da_time, l_freq="AS", u_freq="A", td=0):
    da = da_time.reset_coords(drop=True)
    ll = basics().date_range(
        start=start,
        end=end,
        frequency=l_freq,
    ) - timedelta(hours=td)
    ul = basics().date_range(
        start=start,
        end=end,
        frequency=u_freq,
    ) + timedelta(hours=td)
    lower = xr.DataArray(ll, coords=da.coords, dims=da.dims)
    upper = xr.DataArray(ul, coords=da.coords, dims=da.dims)
    bounds = xr.concat([lower, upper], dim="bnds")
    return bounds.transpose(..., "bnds")
