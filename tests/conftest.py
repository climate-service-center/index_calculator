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


def hurs_series(values):
    def _hurs_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="hurs",
            attrs={
                "standard_name": "relative_humidity",
                "cell_methods": "time: mean",
                "units": "%",
            },
        )

    return _hurs_series(values)


def rsds_series(values):
    def _rsds_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="rsds",
            attrs={
                "standard_name": "surface_downwelling_shortwave_flux",
                "cell_methods": "time: mean",
                "units": "W m-2",
            },
        )

    return _rsds_series(values)


def rsus_series(values):
    def _rsus_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="rsus",
            attrs={
                "standard_name": "surface_upwelling_shortwave_flux",
                "cell_methods": "time: mean",
                "units": "W m-2",
            },
        )

    return _rsus_series(values)


def rlds_series(values):
    def _rlds_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="rlds",
            attrs={
                "standard_name": "surface_downwelling_longwave_flux",
                "cell_methods": "time: mean",
                "units": "W m-2",
            },
        )

    return _rlds_series(values)


def rlus_series(values):
    def _rlus_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="rlus",
            attrs={
                "standard_name": "surface_upwelling_longwave_flux",
                "cell_methods": "time: mean",
                "units": "W m-2",
            },
        )

    return _rlus_series(values)


def sfcWind_series(values):
    def _sfcWind_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="sfcWind",
            attrs={
                "standard_name": "wind_speed",
                "cell_methods": "time: mean",
                "units": "m s-1",
            },
        )

    return _sfcWind_series(values)


def mrt_series(values):
    def _mrt_series(values, start="1/1/2000"):
        coords = pd.date_range(start, periods=len(values), freq="D")
        return xr.DataArray(
            values,
            coords=[coords],
            dims="time",
            name="mrt",
            attrs={
                "standard_name": "mean_radiant_temperature",
                "cell_methods": "time: mean",
                "units": "K",
            },
        )

    return _mrt_series(values)
