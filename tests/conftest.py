import pandas as pd
import xarray as xr


def tas_series(values):
    def _tas_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="tas",
            attrs={
                "standard_name": "air_temperature",
                "cell_methods": "time: mean within days",
                "units": "K",
            },
        )

    return _tas_series(values)


def pr_series(values):
    def _pr_series(values, start="1/1/2000", units="kg m-2 s-1"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="pr",
            attrs={
                "standard_name": "precipitation_flux",
                "cell_methods": "time: mean within days",
                "units": units,
            },
        )

    return _pr_series(values)


def tasmin_series(values):
    def _tasmin_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="tasmin",
            attrs={
                "standard_name": "air_temperature",
                "cell_methods": "time: minimum within days",
                "units": "K",
            },
        )

    return _tasmin_series(values)


def tasmax_series(values):
    def _tasmax_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="tasmax",
            attrs={
                "standard_name": "air_temperature",
                "cell_methods": "time: maximum within days",
                "units": "K",
            },
        )

    return _tasmax_series(values)


def prsn_series(values):
    def _prsn_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="prsn",
            attrs={
                "standard_name": "snowfall_flux",
                "cell_methods": "time: mean",
                "units": "kg m-2 s-1",
            },
        )

    return _prsn_series(values)


def snd_series(values):
    def _snd_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="snd",
            attrs={
                "standard_name": "surface_snow_thickness",
                "cell_methods": "time: mean",
                "units": "m",
            },
        )

    return _snd_series(values)
