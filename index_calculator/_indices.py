from inspect import signature
from warnings import warn

import dask  # noqa
import xarray as xr
import xclim as xc
from xclim.core.calendar import percentile_doy, resample_doy
from xclim.core.units import convert_units_to
from xclim.indices.generic import compare

from ._consts import _base_period as BASE_PERIOD


def _thresh_string(thresh, units):
    if isinstance(thresh, str):
        return thresh
    else:
        return "{} {}".format(str(thresh), units)


def _filter_out_small_values(da, thresh, context=None):
    thresh = convert_units_to(thresh, da, context=context)
    return da.where(da > thresh)


def _get_da(dictionary, var):
    if "ds" in dictionary.keys():
        return dictionary["ds"][var]
    elif var in dictionary.keys():
        return dictionary[var]
    raise ValueError("Variable {} not found!")


def _get_percentile(da, per, base_period_time_range):
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


def _clean_up_params(params, func):
    del_list = []
    for param in params.keys():
        if param not in signature(func).parameters.keys():
            warn(
                "Function {} does not provide parameter {}\n"
                "The parameter will be deleted \n"
                "from parameter list".format(func, param)
            )
            del_list.append(param)
    for param in del_list:
        del params[param]
    return params


class CD:
    """Number of cold and dry days (tas, pr)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.cold_and_dry_days

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        pr_per=None,
        **params,
    ):
        """Calculate number of cold and dry days.

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Mean temperature 25th percentile reference value below which
            a day is considered as a cold day.
        pr_per: xr.DataArray, optional
            Precipitation 25th percentile reference value below which
            a day is considered as a dry day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tas_per` and/or `pr_per`.
            This will be used only if `tas_per` and/or `pr_per` is None.

        Returns
        -------
        xarray.DataArray:
            Number of days where cold and dry conditions coincide.
            If temperature is below {tas_per} a day is considered as a
            cold day.
            If precipitation is below {pr_per} a day is considered as a
            dry day.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.cold_and_dry_days
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tas_per is None:
            da_tas = _get_da(params, "tas")
            tas_per = _get_percentile(
                da=da_tas,
                per=25,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
            da_pr = _get_da(params, "pr")
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            pr_per = _get_percentile(
                da=da_pr_f,
                per=25,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class CDD:
    """Maximum consecutive dry days (pr)."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.maximum_consecutive_dry_days

    def compute(self, thresh=None, **params):
        """Calculate maximum consecutive dry days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Maximum consecutive dry days (precipitation < {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.maximum_consecutive_dry_days
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class CFD:
    """Maximum number of consecutive frost days (tasmin)."""

    def __init__(self):
        self.func = xc.atmos.consecutive_frost_days

    def compute(self, **params):
        """Calculate maximum number of consecutive frost days.

        Returns
        -------
        xarray.DataArray
            Maximum number of consecutive frost days (tasmin < 0 degC).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.consecutive_frost_days
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class CHDYYx:
    """Maximum number of consecutive heat days (tasmax)."""

    def __init__(self):
        self.thresh = 30
        self.func = xc.atmos.maximum_consecutive_warm_days

    def compute(self, thresh=None, **params):
        """Calculate maximum number of consecutive heat days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a heat day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.

        Returns
        -------
        xarray.DataArray
            Maximum number of consecutive heat days (tasmax > {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.maximum_consecutive_warm_days
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(thresh=thresh, **params)


class CSDI:
    """Cold spell duration index (tasmin)."""

    def __init__(self):
        self.window = 6
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.cold_spell_duration_index

    def compute(
        self,
        window=None,
        base_period_time_range=None,
        tasmin_per=None,
        **params,
    ):
        """Calculate cold spell duration index.

        Parameters
        ----------
        window: int, optional
            Minimum number of days with temperature below `tasmin_per`
            to qualify as a cold spell (default: 6).
        tasmin_per: xr.DataArray, optional
            Minimum temperature 10th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tasmin_per`.
            This will be used only if `tasmin_per` is None.

        Returns
        -------
        xarray.DataArray
            Number of days part of a 10th percentile cold spell.
            At least {window} consecutive days.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.cold_spell_duration_index
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if window is None:
            window = self.window
        if tasmin_per is None:
            da = _get_da(params, "tasmin")
            tasmin_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tasmin_per=tasmin_per,
                window=window,
                **params,
            )


class CSU:
    """Maximum consecutive summer days (tasmax)."""

    def __init__(self):
        self.thresh = 25
        self.func = xc.atmos.maximum_consecutive_warm_days

    def compute(self, thresh=None, **params):
        """Calculate maximum consecutive summer days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold  maximum temperature above which a day is considered
            as a summer day (default: 25 degC).
            If type of threshold is an integer the unit is set to degC.

        Returns
        -------
        xarray.DataArray
            Maximum consecutive summer days (tasmax > {thresh}).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.maximum_consecutive_warm_days
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class CW:
    """Number of cold and wet days (tas, pr)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.cold_and_wet_days

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        pr_per=None,
        **params,
    ):
        """Calculate number of cold and wet days.

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Mean temperature 25th percentile reference value below which
            a day is considered as a cold day.
        pr_per: xr.DataArray, optional
            Precipitation 75th percentile reference value above which
            a day is considered as a wet day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tas_per` and/or `pr_per`.
            This will be used only if `tas_per` and/or `pr_per` is None.

        Returns
        -------
        xarray.DataArray:
            Number of days where cold and wet conditions coincide.
            If temperature is below {tas_per} a day is considered as a
            cold day.
            If precipitation is above {pr_per} a day is considered as a
            wet day.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.cold_and_wet_days
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tas_per is None:
            da_tas = _get_da(params, "tas")
            tas_per = _get_percentile(
                da=da_tas,
                per=25,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
            da_pr = _get_da(params, "pr")
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            pr_per = _get_percentile(
                da=da_pr_f,
                per=75,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class CWD:
    """Consecutive wet days (pr)."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.maximum_consecutive_wet_days

    def compute(self, thresh=None, **params):
        """Calculate maximum consecutive wet days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation at or above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Maximum consecutive wet days (pr >= {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.maximum_consecutive_wet_days
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class DD:
    """Number of dry days (pr)."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.dry_days

    def compute(self, thresh=None, **params):
        """Calculate number of dry days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Number of dry days (pr < {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.dry_days
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class DSf:
    """Number of dry spells (pr)."""

    def __init__(self):
        self.thresh = 1
        self.window = 5
        self.func = xc.atmos.dry_spell_frequency

    def compute(self, thresh=None, window=None, **params):
        """Calculate number of dry spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int, optional
            Minimum number of days with precipitation below threshold
            to qualify as a dry spell (default: 5).

        Returns
        -------
        xarray.DataArray
            Number of dry periods of minimum {window} days (pr < {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.dry_spell_frequency
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "mm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class DSx:
    """Maximum length of dry spells (pr)."""

    def __init__(self):
        self.thresh = 1
        self.window = 1
        self.func = xc.atmos.dry_spell_max_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate maximum length of dry spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int, optional
            Minimum number of days with precipitation below threshold
            to qualify as a dry spell (default: 1).

        Returns
        -------
        xarray.DataArray
            Maximum length of dry spells of at least {window} consecutive days
            with precipitation below {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.dry_spell_max_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "mm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class DSn:
    """Total number of days in dry spells (pr)."""

    def __init__(self):
        self.thresh = 1
        self.window = 5
        self.func = xc.atmos.dry_spell_total_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate total number of days in dry spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int, optional
            Minimum number of days with precipitation below threshold
            to qualify as a dry spell (default: 5).

        Returns
        -------
        xarray.DataArray
            Total number of days in dry spells of at least {window}
            consecutive days with precipitation below {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.dry_spell_total_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "mm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class WSf:
    """Number of wet spells (pr)."""

    def __init__(self):
        self.thresh = 1
        self.window = 5
        self.func = xc.atmos.wet_spell_frequency

    def compute(self, thresh=None, window=None, **params):
        """Calculate number of wet spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int, optional
            Minimum number of days with precipitation above threshold
            to qualify as a wet spell (default: 5).

        Returns
        -------
        xarray.DataArray
            Number of wet periods of minimum {window} days (pr >= {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wet_spell_frequency
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "mm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class WSx:
    """Maximum length of wet spells (pr)."""

    def __init__(self):
        self.thresh = 1
        self.window = 1
        self.func = xc.atmos.wet_spell_max_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate maximum length of wet spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int, optional
            Minimum number of days with precipitation above threshold
            to qualify as a wet spell (default: 1).

        Returns
        -------
        xarray.DataArray
            Maximum length of wet spells of at least {window} consecutive days
            with precipitation above {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wet_spell_max_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            thresh = self.window
        thresh = _thresh_string(thresh, "mm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class WSn:
    """Total number of days in wet spells (pr)."""

    def __init__(self):
        self.thresh = 1
        self.window = 5
        self.func = xc.atmos.wet_spell_total_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate total number of days in wet spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int, optional
            Minimum number of days with precipitation above threshold
            to qualify as a wet spell (default: 5).

        Returns
        -------
        xarray.DataArray
            Total numer of days in wet spells of at least {window}
            consecutive days with precipitation above {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wet_spell_total_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "mm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class DTR:
    """Mean temperature rnage (tasmax, tasmin)."""

    def __init__(self):
        self.func = xc.atmos.daily_temperature_range

    def compute(self, **params):
        """Calculate mean of daily temperature range.

        Returns
        -------
        xarray.DataArray
            Mean of daily temperature range.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.daily_temperature_range
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class FD:
    """Number of frost days (tasmin)."""

    def __init__(self):
        self.func = xc.atmos.frost_days

    def compute(self, **params):
        """Calculate number of frost days (tasmin < 0.0 degC).

        Returns
        -------
        xarray.DataArray
            Number of frost days (tasmin < 0.0 degC).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.frost_days
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class LFD:
    """Number of late frost days (tasmin)."""

    def __init__(self):
        self.start_date = "04-01"
        self.end_date = "06-30"
        self.func = xc.atmos.late_frost_days

    def compute(self, start_date=None, end_date=None, **params):
        """Calculate number of late frost days (tasmin < 0.0 degC).

        Parameters
        ----------
        start_date: str, optional
            Left bound of the period to be considered.
        end_date: str, optional
            Right bound of the period to be considered.

        Returns
        -------
        xarray.DataArray
            Number of frost days (tasmin < 0.0)
            between {start_date} and {end_date}.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.late_frost_days
        """
        if start_date is None:
            start_date = self.start_date
        if end_date is None:
            end_date = self.end_date

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            date_bounds=(start_date, end_date),
            **params,
        )


class ID:
    """Number of ice days (tasmax)."""

    def __init__(self):
        self.func = xc.atmos.ice_days

    def compute(self, **params):
        """Calculate number of ice days (tasmax < 0.0 degC).

        Parameters
        ----------
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.ice_days

        Returns
        -------
        xarray.DataArray
            Number of ice days (tasmax < 0.0 degC).
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class GD:
    """Cumulative growing degree days (tas)."""

    def __init__(self):
        self.thresh = 4
        self.func = xc.atmos.growing_degree_days

    def compute(self, thresh=None, **params):
        """Calculate cumulative growing degree days (tas > thresh).

        Parameters
        ----------
        thresh: int or string, optional
            Threshold temperature above which the daily temperature will
            be added to the cumulative sum of temperature degrees.

        Returns
        -------
        xarray.DataArray
            Cumulative growing degree days (tas > {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.growing_degree_days
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class HD17:
    """Cumulative heating degree days (tas)."""

    def __init__(self):
        self.func = xc.atmos.heating_degree_days

    def compute(self, **params):
        """Calculate cumulative heating degree days (tas < 17 degC).

        Returns
        -------
        xarray.DataArray
            Cumulative heating degree days (tas > 17 degC).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.heating_degree_days
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class PRCPTOT:
    """Total precipitation amount (pr)."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.wet_precip_accumulation

    def compute(self, thresh=None, **params):
        """Calculate total precipitation amount.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Total precipitation amount of wet days (precip > {thresh})

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wet_precip_accumulation
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class RR:
    """Total precipitation (pr)."""

    def __init__(self):
        self.func = xc.atmos.precip_accumulation

    def compute(self, **params):
        """Calculate total precipitation.

        Returns
        -------
        xarray.DataArray
            Total precipitation.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.precip_accumulation
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class RRm:
    """Mean daily precipitation (pr)."""

    def __init__(self):
        self.func = xc.atmos.precip_average

    def compute(self, **params):
        """Calculate mean daily precipitation.

        Returns
        -------
        xarray.DataArray
            Mean daily precipitation.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.precip_average
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class RR1:
    """Number of wet days (pr)."""

    def __init__(self):
        self.func = xc.atmos.wetdays

    def compute(self, **params):
        """Calculate number of wet days (pr >= 1 mm/day).

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 1 mm/day).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wetdays
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh="1 mm/day",
            **params,
        )


class R10mm:
    """Number of heavy precipitation days (pr)."""

    def __init__(self):
        self.func = xc.atmos.wetdays

    def compute(self, **params):
        """Calculate number of wet days (pr >= 10 mm/day).

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 10 mm/day).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wetdays
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh="10 mm/day",
            **params,
        )


class R20mm:
    """Number of very heavy precipitation days (pr)."""

    def __init__(self):
        self.func = xc.atmos.wetdays

    def compute(self, **params):
        """Calculate number of wet days (pr >= 20 mm/day).

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 20 mm/day).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wetdays
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh="20 mm/day",
            **params,
        )


class R25mm:
    """Number of super heavy precipitation days (pr)."""

    def __init__(self):
        self.func = xc.atmos.wetdays

    def compute(self, **params):
        """Calculate number of wet days (pr >= 25 mm/day).

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 25 mm/day).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wetdays
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh="25 mm/day",
            **params,
        )


class RRYYp:
    """Precip percentil value for wet days (pr)."""

    def __init__(self):
        self.per = 75
        self.thresh = 1
        self.base_period_time_range = BASE_PERIOD
        self.func = _get_percentile

    def compute(
        self,
        per=None,
        thresh=None,
        base_period_time_range=None,
        **params,
    ):
        """Calculate precip percentile reference value
        for wet days (pr > thresh).

        Parameters
        ----------
        per: int, optional
            Percentile value.
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating the precip percentile
            reference value.

        Returns
        -------
        xarray.DataArray
            Precip {per}th percentil reference value
            for wet days (pr > {thresh}).
        """
        if per is None:
            per = self.per
        if thresh is None:
            thresh = self.thresh
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da = _filter_out_small_values(da, thresh, context="hydro")
        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            da=da,
            per=per,
            base_period_time_range=base_period_time_range,
        )


class RYYp:
    """Number of wet days with precip over a given percentile (pr)."""

    def __init__(self):
        self.per = 75
        self.thresh = 1
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.days_over_precip_doy_thresh

    def compute(
        self,
        per=None,
        thresh=None,
        base_period_time_range=None,
        **params,
    ):
        """Calculate number of wet days (pr > thresh)
        with precip over a given percentile.

        Parameters
        ----------
        per: int, optional
            Precipitation percentile value.
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating the precip
            percentile reference value.

        Returns
        -------
        xarray.DataArray
            Number of wet days (pyr > {thresh}) over a {per}th percentile.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.days_over_precip_doy_thresh
        """
        if per is None:
            per = self.per
        if thresh is None:
            thresh = self.thresh
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, thresh, context="hydro")
        pr_per = _get_percentile(
            da=da_pr,
            per=per,
            base_period_time_range=base_period_time_range,
        )

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            pr_per=pr_per,
            **params,
        )


class RYYmm:
    """Number of days with precip over threshold (pr)."""

    def __init__(self):
        self.thresh = 25
        self.func = xc.atmos.wetdays

    def compute(self, thresh=None, **params):
        """Calculate number of wet days.

        Parameters
        ----------
        thresh: int or str, optional
        Threshold precipitation above which a day is considered
            as a wet day (default: 25 mm/day).
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr > {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.wetdays
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class RX1day:
    """Maximum 1-day total precipitation (pr)."""

    def __init__(self):
        self.func = xc.atmos.max_1day_precipitation_amount

    def compute(self, **params):
        """Calculate maximum 1-day total precipitation.

        Returns
        -------
        xarray.DataArray
            Maximum 1-day total precipitation.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.max_1day_precipitation_amount
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class RXYYday:
    """Maximum n-day total precipitation (pr)."""

    def __init__(self):
        self.window = 5
        self.func = xc.atmos.max_n_day_precipitation_amount

    def compute(self, window=None, **params):
        """Calculate maximum {window}-day total precipitation.

        Parameters
        ----------
        window: int, optional
            Window size in days (default: 5).

        Returns
        -------
        xarray.DataArray
            Maximum {window}-day total precipitation.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.max_n_day_precipitation_amount
        """
        if window is None:
            window = self.window

        params = _clean_up_params(params=params, func=self.func)
        return self.func(window=window, **params)


class RYYpABS:
    """Total precipitation amount with precip above percentile
    on wet days (pr)."""

    def __init__(self):
        self.per = 75
        self.thresh = 1
        self.base_period_time_range = BASE_PERIOD

    def compute(
        self,
        per=None,
        thresh=None,
        base_period_time_range=None,
        **params,
    ):
        """Calculate total precipitation amount with
        precip > {perc}th percentile on wet days (pr > thresh).

        Parameters
        ----------
        per: int, optional
            Percentile value.
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calulating the precip percentile
            reference value.

        Returns
        -------
        xarray.DataArray
            Precipitation fraction with precip > {perc}th percentile
            on wet days (pr > {thresh}).
        """
        if per is None:
            per = self.per
        if thresh is None:
            thresh = self.thresh
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, thresh, context="hydro")
        pr_per = _get_percentile(
            da=da_pr,
            per=per,
            base_period_time_range=base_period_time_range,
        )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            pr_per = convert_units_to(pr_per, da, context="hydro")
            thresh = convert_units_to(thresh, da, context="hydro")

            tp = pr_per.where(pr_per > thresh, thresh)
            if "dayofyear" in pr_per.coords:
                # Create time series out of doy values.
                tp = resample_doy(tp, da)

            constrain = (">", ">=")

            # Compute the days when precip is both over the wet day threshold
            # and the percentile threshold.
            over = (
                da.where(compare(da, ">", tp, constrain))
                .resample(time=params["freq"])
                .sum(dim="time")
            )
            out = convert_units_to(over, "mm/day")
            out.attrs["units"] = "mm"
            return out


class RYYpTOT:
    """Precipitation fraction with precip above percentile on wet days (pr)."""

    def __init__(self):
        self.per = 75
        self.thresh = 1
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.fraction_over_precip_thresh

    def compute(
        self,
        per=None,
        thresh=None,
        base_period_time_range=None,
        **params,
    ):
        """Calculate precipitation fraction with precip above percentile
        on wet days (pr > thresh).

        Parameters
        ----------
        per: int, optional
            Percentile value.
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calulating the precip percentile
            reference value.

        Returns
        -------
        xarray.DataArray
            Precipitation fraction with precip > {perc}th percentile
            on wet days (pr > {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.fraction_over_precip_thresh
        """
        if per is None:
            per = self.per
        if thresh is None:
            thresh = self.thresh
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, thresh, context="hydro")
        pr_per = _get_percentile(
            da=da_pr,
            per=per,
            base_period_time_range=base_period_time_range,
        )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                pr_per=pr_per,
                **params,
            )


class SDII:
    """Average precipitation during wet days (pr)."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.daily_pr_intensity

    def compute(self, thresh=None, **params):
        """Calculate average precipitation during wet days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Average precipitation during wet days.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.daily_pr_intensity
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(1, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class SU:
    """Number of summer days (tasmax)."""

    def __init__(self):
        self.thresh = 25
        self.func = xc.atmos.tx_days_above

    def compute(self, thresh=None, **params):
        """Calculate number of summer days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold maximum temperature above which to day is considered
            as a summer day (default: 25 degC).
            If type of threshold is an integer the unit is set to degC.

        Returns
        -------
        xarray.DataArray
            Number of summer days (tx > {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx_days_above
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")
        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class SQI:
    """Number of uncomfortable sleep events (tasmin)."""

    def __init__(self):
        self.thresh = 18
        self.func = xc.atmos.tn_days_above

    def compute(self, thresh=None, **params):
        """Calculate number of uncomfortable sleep events.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold minimum temperature below which a day has
            a uncomfortable sleep event (default: 18 degC).
            If type of threshold is an integer the unit is set to degC.

        Returns
        -------
        xarray.DataArray
            Number of uncomfortable sleep events (tn < {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn_days_above
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class TG:
    """Mean mean temperature (tas)."""

    def __init__(self):
        self.func = xc.atmos.tg_mean

    def compute(self, **params):
        """Calculate mean daily mean temperature.

        Returns
        -------
        xarray.DataArray
            Mean daily mean temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tg_mean
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class TG10p:
    """Fraction of days with mean temperature < 10th percentile (tas)."""

    def __init__(self):
        self.tas_per = None
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.tg10p

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        **params,
    ):
        """Calculate fraction of days with mean temperature < 10th percentile.

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Temperature 10th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound is
            end year string for calculating `tas_per`.
            This will be used only if `tas_per` is None.

        Returns
        -------
        xarray.DataArray
            Fraction of days with mean temperature < 10th percentile".

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tg10p
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tas_per is None:
            da = _get_da(params, "tas")
            tas_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tas_per=tas_per,
                **params,
            )


class TG90p:
    """Fraction of days with mean temperature > 90th percentile (tas)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.tg90p

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        **params,
    ):
        """Calculate fraction of days with mean temperature > 90th percentile".

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Temperature 90th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tas_per`.
            This will be used only if `tas_per` is None.

        Returns
        -------
        xarray.DataArray
            Fraction of days with mean temperature > 90th percentile".

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tg90p
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tas_per is None:
            da = _get_da(params, "tas")
            tas_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tas_per=tas_per,
                **params,
            )


class TR:
    """Number of tropical nights (tasmin)."""

    def __init__(self):
        self.thresh = 20
        self.func = xc.atmos.tn_days_above

    def compute(self, thresh=None, **params):
        """Calculate number of tropical nights.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold minimum temperature on which a day
            has a tropical night (default: 20 degC).
            If type of threshold is an integer the unit is set to degC.

        Returns
        -------
        xarray.DataArray
            Number of tropical nights (tn > {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn_days_above
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class TX:
    """Mean maximum temperature (tasmax)."""

    def __init__(self):
        self.func = xc.atmos.tx_mean

    def compute(self, **params):
        """Calculate mean daily maximum temperature.

        Returns
        -------
        xarray.DataArray
            Mean daily maximum temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx_mean
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class TX10p:
    """Fraction of days with max temperature < 10th percentile (tasmax)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.tx10p

    def compute(
        self,
        base_period_time_range=None,
        tasmax_per=None,
        **params,
    ):
        """Calculate fraction of days with max temperature < 10th percentile.

        Parameters
        ----------
        tasmax_per: xr.DataArray, optional
            Maximum temperature 10th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tasmax_per`.
            This will be used only if `tasmax_per` is None.

        Returns
        -------
        xarray.DataArray
            Fraction of days with maximum temperature < 10th percentile".

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx10p
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tasmax_per is None:
            da = _get_da(params, "tasmax")
            tasmax_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tasmax_per=tasmax_per,
                **params,
            )


class TX90p:
    """Fraction of days with max temperature > 90th percentile (tasmax)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.tx90p

    def compute(
        self,
        base_period_time_range=None,
        tasmax_per=None,
        **params,
    ):
        """Calculate fraction of days with max temperature > 90th percentile.

        Parameters
        ----------
        tasmax_per: xr.DataArray, optional
            Maximum temperature 90th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tasmax_per`.
            This will be used only if `tasmax_per` is None.

        Returns
        -------
        xarray.DataArray
            Fraction of days with maximum temperature > 90th percentile".

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx90p
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tasmax_per is None:
            da = _get_da(params, "tasmax")
            tasmax_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tasmax_per=tasmax_per,
                **params,
            )


class TXn:
    """Minimum maximum temperature (tasmax)."""

    def __init__(self):
        self.func = xc.atmos.tx_min

    def compute(self, **params):
        """Calculate minimum daily maximum temperature.

        Returns
        -------
        xarray.DataArray
            Minimum daily maximum temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx_min
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class TXx:
    """Maximum maximum temperature (tasmax)."""

    def __init__(self):
        self.func = xc.atmos.tx_max

    def compute(self, **params):
        """Calculate maximum daily maximum temperature.

        Returns
        -------
        xarray.DataArray
            Maximum daily maximum temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx_max
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class TN:
    """Mean minimum temperature (tasmin)."""

    def __init__(self):
        self.func = xc.atmos.tn_mean

    def compute(self, **params):
        """Calculate mean daily minimum temperature.

        Returns
        -------
        xarray.DataArray
            Mean daily minimum temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn_mean
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class TN10p:
    """Fraction of days with min temperature < 10th percentile."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.tn10p

    def compute(
        self,
        base_period_time_range=None,
        tasmin_per=None,
        **params,
    ):
        """Calculate fraction of days with min temperature < 10th percentile.

        Parameters
        ----------
        tasmin_per: xr.DataArray, optional
            Minimum temperature 10th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tasmin_per`.
            This will be used only if `tasmin_per` is None.

        Returns
        -------
        xarray.DataArray
            Fraction of days with minimum temperature < 10th percentile".

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn10p
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tasmin_per is None:
            da = _get_da(params, "tasmin")
            tasmin_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tasmin_per=tasmin_per,
                **params,
            )


class TN90p:
    """Fraction of days with min temperature > 90th percentile."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.tn90p

    def compute(
        self,
        base_period_time_range=None,
        tasmin_per=None,
        **params,
    ):
        """Calculate fraction of days with min temperature > 90th percentile.

        Parameters
        ----------
        tasmin_per: xr.DataArray, optional
            Minimum temperature 90th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tasmin_per`.
            This will be used only if `tasmin_per` is None.

        Returns
        -------
        xarray.DataArray
            Fraction of days with minimum temperature > 90th percentile".

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tx90p
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tasmin_per is None:
            da = _get_da(params, "tasmin")
            tasmin_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tasmin_per=tasmin_per,
                **params,
            )


class TNn:
    """Minimum minimum temperature (tasmin)."""

    def __init__(self):
        self.func = xc.atmos.tn_min

    def compute(self, **params):
        """Calculate minimum daily minimum temperature.

        Returns
        -------
        xarray.DataArray
            Minimum daily minimum temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn_min
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class TNx:
    """Maximum minimum temperature (tasmin)."""

    def __init__(self):
        self.func = xc.atmos.tn_max

    def compute(self, **params):
        """Calculate maximum daily minimum temperature.

        Returns
        -------
        xarray.DataArray
            Maximum daily minimum temperature.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn_max
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class WD:
    """Number of warm and dry days (tas, pr)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.warm_and_dry_days

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        pr_per=None,
        **params,
    ):
        """Calculate number of warm and dry days.

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Mean temperature 75th percentile reference value above which
            a day is considered as a warm day.
        pr_per: xr.DataArray, optional
            Precipitation 25th percentile reference value below which
            a day is considered as a dry day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tas_per` and/or `pr_per`.
            This will be used only if `tas_per` and/or `pr_per` is None.

        Returns
        -------
        xarray.DataArray:
            Number of days where warm and dry conditions coincide.
            If temperature is above {tas_per} a day is considered as a
            warm day.
            If precipitation is below {pr_per} a day is considered as a
            dry day.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.warm_and_dry_days
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tas_per is None:
            da_tas = _get_da(params, "tas")
            tas_per = _get_percentile(
                da=da_tas,
                per=75,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
            da_pr = _get_da(params, "pr")
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            pr_per = _get_percentile(
                da=da_pr_f,
                per=25,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class WSDI:
    """Warm spell duration index (tasmax)."""

    def __init__(self):
        self.window = 6
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.warm_spell_duration_index

    def compute(
        self,
        window=None,
        base_period_time_range=None,
        tasmax_per=None,
        **params,
    ):
        """Calculate warm spell duration index.

        Parameters
        ----------
        window: int, optional
            Minimum number of days with temperature above `tasmax_per`
            to qualify as a warm spell (default: 6).
        tasmin_per: xr.DataArray, optional
            Maximum temperature 90th percentile reference value.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tasmax_per`.
            This will be used only if `tasmax_per` is None.

        Returns
        -------
        xarray.DataArray
            Number of days part of a 90th percentile warm spell.
            At least {window} consecutive days.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.warm_spell_duration_index
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if window is None:
            window = self.window
        if tasmax_per is None:
            da = _get_da(params, "tasmax")
            tasmax_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tasmax_per=tasmax_per,
                window=window,
                **params,
            )


class WW:
    """Number of warm and wet days (tas, pr)."""

    def __init__(self):
        self.base_period_time_range = BASE_PERIOD
        self.func = xc.atmos.warm_and_wet_days

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        pr_per=None,
        **params,
    ):
        """Calculate number of warm and wet days.

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Mean temperature 75th percentile reference value above which
            a day is considered as a warm day.
        pr_per: xr.DataArray, optional
            Precipitation 75th percentile reference value above which
            a day is considered as a wet day.
        base_period_time_range: list, optional
            List with left bound is start year string and right bound
            is end year string for calculating `tas_per` and/or `pr_per`.
            This will be used only if `tas_per` and/or `pr_per` is None.

        Returns
        -------
        xarray.DataArray:
            Number of days where warm and wet conditions coincide.
            If temperature is above {tas_per} a day is considered as a
            warm day.
            If precipitation is above {pr_per} a day is considered as a
            wet day.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.warm_and_wet_days
        """
        if base_period_time_range is None:
            base_period_time_range = self.base_period_time_range
        if tas_per is None:
            da_tas = _get_da(params, "tas")
            tas_per = _get_percentile(
                da=da_tas,
                per=75,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
            da_pr = _get_da(params, "pr")
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            pr_per = _get_percentile(
                da=da_pr_f,
                per=75,
                base_period_time_range=base_period_time_range,
            )

        params = _clean_up_params(params=params, func=self.func)
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return self.func(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class CSf:
    """Number of cold spells (tas)."""

    def __init__(self):
        self.thresh = -10
        self.window = 3
        self.func = xc.atmos.cold_spell_frequency

    def compute(self, thresh=None, window=None, **params):
        """Calculate number of cold spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold temperature below which a day is considered
            as a cold day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature below thresh
            to qualify as a cold spell (default: 3).

        Returns
        -------
        xarray.DataArray
            Number of cold spells of at least {window} consecutive days
            with temperature below {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.cold_spell_frequency
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class CSx:
    """Maximum length of cold spells (tas)."""

    def __init__(self):
        self.thresh = -10
        self.window = 1
        self.func = xc.atmos.cold_spell_max_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate maximum length of cold spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold temperature below which a day is considered
            as a cold day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature below thresh
            to qualify as a cold spell (default: 1).

        Returns
        -------
        xarray.DataArray
            Number of cold spells of at least {window} consecutive days
            with temperature below {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.cold_spell_max_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class CSn:
    """Total number of days in cold spells (tas)."""

    def __init__(self):
        self.thresh = -10
        self.window = 3
        self.func = xc.atmos.cold_spell_total_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate total number of days in cold spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold temperature below which a day is considered
            as a cold day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature below thresh
            to qualify as a cold spell (default: 3).

        Returns
        -------
        xarray.DataArray
            Total number of days in cold spells of at least {window}
            consecutive days with temperature below {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.cold_spell_total_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class HSf:
    """Number of hot spells (tasmax)."""

    def __init__(self):
        self.thresh = 35
        self.window = 3
        self.func = xc.atmos.hot_spell_frequency

    def compute(self, thresh=None, window=None, **params):
        """Calculate number of hot spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a hot day (default: 35 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above thresh
            to qualify as a hot spell (default: 3).

        Returns
        -------
        xarray.DataArray
            Number of hot spells of at least {window} consecutive days
            with maximum temperature above {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.hot_spell_frequency
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class HSx:
    """Maximum lenght of hot spells (tasmax)."""

    def __init__(self):
        self.thresh = 35
        self.window = 1
        self.func = xc.atmos.hot_spell_max_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate maximum lenght of hot spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a hot day (default: 35 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above thresh
            to qualify as a hot spell (default: 1).

        Returns
        -------
        xarray.DataArray
            Maximum length of hot spells of at least {window}
            consecutive days with maximum temperature above {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.hot_spell_max_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class HSn:
    """Total number of days in hot spells (tasmax)."""

    def __init__(self):
        self.thresh = 35
        self.window = 3
        self.func = xc.atmos.hot_spell_total_length

    def compute(self, thresh=None, window=None, **params):
        """Calculate total number of days in hot spells.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a hot day (default: 35 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above thresh
            to qualify as a hot spell (default: 3).

        Returns
        -------
        xarray.DataArray
            Total number of  days in hot spells of at least {window}
            consecutive days with maximum temperature above {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.hot_spell_total_length
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class SD:
    """Number of snow days."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.days_with_snow

    def compute(self, thresh=None, **params):
        """Calculate number of snow days.

        Parameters
        ----------
        thresh: int or string
            Liquid water equivalent snowfall rate above which a day is
            considered as a snow day (default: 1 mm/day) .
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Number of days with solid precipitation flux
            above {thresh} threshold.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.days_with_snow
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            low=thresh,
            **params,
        )


class SCD:
    """Snow cover duration."""

    def __init__(self):
        self.thresh = 3
        self.func = xc.land.snd_season_length

    def compute(
        self,
        thresh=None,
        **params,
    ):
        """Calculate snow cover duration.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold snow thickness above which a day is considered
            as a snow day (default: 3 cm).
            If type of threshold is an integer the unit is set to cm.

        Returns
        -------
        xarray.DataArray
            Number of days with snow cover above {thresh} threshold.
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "cm")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class Sint:
    """Snowfall intensity."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.snowfall_intensity

    def compute(self, thresh=None, **params):
        """Calculate snowfall intensity.

        Parameters
        ----------
        thresh: int or string, optional
            Liquid water equivalent snowfall rate above which a day is
            considered as a snow day (default: 1 mm/day) .
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Mean daily snowfall during days with snowfall > {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.snowfall_intensity
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class Sfreq:
    """Snowfall frequency."""

    def __init__(self):
        self.thresh = 1
        self.func = xc.atmos.snowfall_frequency

    def compute(self, thresh=None, **params):
        """Calculate snowfall frequency.

        Parameters
        ----------
        thresh: int or string, optional
            Liquid water equivalent snowfall rate above which a day is
            considered as a snow day (default: 1 mm/day) .
            If type of threshold is an integer the unit is set to mm/day.

        Returns
        -------
        xarray.DataArray
            Percentage of days with snowfall > {thresh}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.snowfall_frequency
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "mm/day")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class UTCI:
    """Universal thermal climate index."""

    def __init__(self):
        self.stat = "average"
        self.mask_invalid = True
        self.func = xc.atmos.universal_thermal_climate_index

    def compute(self, stat=None, mask_invalid=None, **params):
        """Calculate universal thermal climate index.

        Parameters
        ----------
        stat: {‘average’, ‘sunlit’, ‘instant’}, optional
            Which statistic to apply. If “average”, the average of the cosine
            of the solar zenith angle is calculated.
            If “instant”, the instantaneous cosine of the solar zenith angle is
            calculated.
            If “sunlit”, the cosine of the solar zenith angle is calculated
            during the sunlit period of each interval.
            If “instant”, the instantaneous cosine of the solar zenith angle is
            calculated.
            This is necessary if mrt is not None (default: average).
        mask_valid: bool, optional
            If True, UTCI values are NaN where any of the inputs are outside
            their validity ranges:
            -50°C < tas < 50°C,
            -30°C < tas - mrt < 30°C
            0.5 m/s < sfcWind < 17.0 m/s
            (default: True).

        Returns
        -------
        xarray.DataArray
            Universal Thermal Climate Index.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.universal_thermal_climate_index
        """
        if stat is None:
            stat = self.stat
        if mask_invalid is None:
            mask_invalid = self.mask_invalid

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            stat=stat,
            mask_invalid=mask_invalid,
            **params,
        )


class WI:
    """Number of winter days (tasmin)."""

    def __init__(self):
        self.thresh = -10
        self.func = xc.atmos.tn_days_below

    def compute(self, thresh=None, **params):
        """Calculate number of winter days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold minimum temperature below which a day is considered
            as a winter day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.

        Returns
        -------
        xarray.DataArray
            Number of winter days.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.tn_days_below
        """
        if thresh is None:
            thresh = self.thresh
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            **params,
        )


class HWf:
    """Number of heat waves (tasmax, tasmin)."""

    def __init__(self):
        self.thresh_tasmin = 22
        self.thresh_tasmax = 30
        self.window = 3
        self.func = xc.atmos.heat_wave_frequency

    def compute(
        self,
        thresh_tasmin=None,
        thresh_tasmax=None,
        window=None,
        **params,
    ):
        """Calculate number of heat waves.

        Parameters
        ----------
        thresh_tasmin: int or string, optional
            Threshold minimum temperature above which a day is considered
            as a heat day (default: 22 degC).
            If type of threshold is an integer the unit is set to degC.
        thresh_tasmax: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a winter day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above thresh
            to qualify as a hot spell (default: 3).

        Returns
        -------
        xarray.DataArray
            Number of heat waves of at least {window} consecutive days
            with maximum temperature above {thresh_tasmax} and
            minimum temperature above {thresh_tasmin}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.hot_spell_frequency
        """
        if thresh_tasmax is None:
            thresh_tasmax = self.thresh_tasmax
        if thresh_tasmin is None:
            thresh_tasmin = self.thresh_tasmin
        if window is None:
            window = self.window
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
            window=window,
            **params,
        )


class HWx:
    """Maximum length of heat waves (tasmax, tasmin)."""

    def __init__(self):
        self.thresh_tasmin = 22
        self.thresh_tasmax = 30
        self.window = 1
        self.func = xc.atmos.heat_wave_max_length

    def compute(
        self,
        thresh_tasmax=None,
        thresh_tasmin=None,
        window=None,
        **params,
    ):
        """Calculate maximum number of heat waves.

        Parameters
        ----------
        thresh_tasmin: int or string, optional
            Threshold minimum temperature above which a day is considered
            as a heat day (default: 22 degC).
            If type of threshold is an integer the unit is set to degC.
        thresh_tasmax: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a winter day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above thresh
            to qualify as a hot spell (default: 1).

        Returns
        -------
        xarray.DataArray
            Maximum length of heat waves of at least {window} consecutive days
            with maximum temperature above {thresh_tasmax} and
            minimum temperature above {thresh_tasmin}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.heat_wave_max_length
        """
        if thresh_tasmax is None:
            thresh_tasmax = self.thresh_tasmax
        if thresh_tasmin is None:
            thresh_tasmin = self.thresh_tasmax
        if window is None:
            window = self.window
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
            window=window,
            **params,
        )


class HWn:
    """Total number of days in heat waves (tasmax, tasmin)."""

    def __init__(self):
        self.thresh_tasmin = 22
        self.thresh_tasmax = 30
        self.window = 3
        self.func = xc.atmos.heat_wave_total_length

    def compute(
        self,
        thresh_tasmin=None,
        thresh_tasmax=None,
        window=None,
        **params,
    ):
        """Calculate total number of days in heat waves.

        Parameters
        ----------
        thresh_tasmin: int or string, optional
            Threshold minimum temperature above which a day is considered
            as a heat day (default: 22 degC).
            If type of threshold is an integer the unit is set to degC.
        thresh_tasmax: int or string, optional
            Threshold maximum temperature above which a day is considered
            as a winter day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above thresh
            to qualify as a hot spell (default: 3).

        Returns
        -------
        xarray.DataArray
            Total number of days in heat waves of at least {window}
            consecutive days with maximum temperature above {thresh_tasmax}
            and minimum temperature above {thresh_tasmin}.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.hot_spell_total_length
        """
        if thresh_tasmax is None:
            thresh_tasmax = self.thresh_tasmax
        if thresh_tasmin is None:
            thresh_tasmin = self.thresh_tasmin
        if window is None:
            window = self.window
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
            window=window,
            **params,
        )


class GSS:
    """Growing season start (tas)."""

    def __init__(self):
        self.thresh = 5
        self.window = 5
        self.func = xc.atmos.growing_season_start

    def compute(self, thresh=None, window=None, **params):
        """Calculate growing season start.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold temperature above which the growing season starts
            (default: 5 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above threshold
            needed for evaluation (default: 5).

        Returns
        -------
        xarray.DataArray
            Growing season start.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.growing_season_start
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class GSE:
    """Growing season end (tas)."""

    def __init__(self):
        self.thresh = 5
        self.window = 5
        self.func = xc.atmos.growing_season_end

    def compute(self, thresh=None, window=None, **params):
        """Calculate growing season end.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold temperature below which the growing season ends
            (default: 5 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature below threshold
            needed for evaluation (default: 5).

        Returns
        -------
        xarray.DataArray
            Growing season end.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.growing_season_end
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class FFS:
    """Frost free season start (tasmin)."""

    def __init__(self):
        self.thresh = 0
        self.window = 5
        self.func = xc.atmos.frost_free_season_start

    def compute(self, thresh=None, window=None, **params):
        """Calculate frost free season start.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold minimum temperature above which the frost free season
            starts (default: 0 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature above threshold
            needed for evaluation (default: 5).

        Returns
        -------
        xarray.DataArray
            Frost free season start.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.frost_free_season_start
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class FFE:
    """Frost free season end (tasmin)."""

    def __init__(self):
        self.thresh = 0
        self.window = 5
        self.func = xc.atmos.frost_free_season_end

    def compute(self, thresh=None, window=None, **params):
        """Calculate frost free season end.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold minimum temperature below which the frost free season
            ends (default: 0 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int, optional
            Minimum number of days with temperature below threshold
            needed for evaluation (default: 5).

        Returns
        -------
        xarray.DataArray
            Frost free season end.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.frost_free_season_end
        """
        if thresh is None:
            thresh = self.thresh
        if window is None:
            window = self.window
        thresh = _thresh_string(thresh, "degC")

        params = _clean_up_params(params=params, func=self.func)
        return self.func(
            thresh=thresh,
            window=window,
            **params,
        )


class FG:
    """Mean daily mean wind speed."""

    def __init__(self):
        self.func = xc.atmos.sfcWind_mean

    def compute(self, **params):
        """Calculate mean daily mean wind speed.

        Returns
        -------
        xarray.DataArray
            Mean daily mean wind speed.

        Notes
        -----
        If sfcWind is not provided in `ds` sfcWind could be computed
        from `ds`.uas and `ds`.vas.

        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.sfcWind_mean
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class FGn:
    """Minimum daily mean wind speed."""

    def __init__(self):
        self.func = xc.atmos.sfcWind_min

    def compute(self, **params):
        """Calculate minimum daily mean wind speed.

        Returns
        -------
        xarray.DataArray
            Minimum daily mean wind speed.

        Notes
        -----
        If sfcWind is not provided in `ds` sfcWind could be computed
        from `ds`.uas and `ds`.vas.

        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.sfcWind_min
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class FGx:
    """Maximum daily mean wind speed."""

    def __init__(self):
        self.func = xc.atmos.sfcWind_max

    def compute(self, **params):
        """Calculate maximum daily mean wind speed.

        Returns
        -------
        xarray.DataArray
            Maximum daily mean wind speed.

        Notes
        -----
        If sfcWind is not provided in `ds` sfcWind could be computed
        from `ds`.uas and `ds`.vas.

        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.sfcWind_max
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class FX:
    """Mean daily maximum wind speed."""

    def __init__(self):
        self.func = xc.atmos.sfcWindmax_mean

    def compute(self, **params):
        """Calculate mean daily maximum wind speed.

        Returns
        -------
        xarray.DataArray
            Mean daily maximum wind speed.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.sfcWindmax_mean
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class FXn:
    """Minimum daily maximum wind speed."""

    def __init__(self):
        self.func = xc.atmos.sfcWindmax_min

    def compute(self, **params):
        """Calculate minimum daily maximum wind speed.

        Returns
        -------
        xarray.DataArray
            Minimum daily maximum wind speed.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.sfcWindmax_min
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)


class FXx:
    """Maximum daily maximum wind speed."""

    def __init__(self):
        self.func = xc.atmos.sfcWindmax_max

    def compute(self, **params):
        """Calculate maximum daily maximum wind speed.

        Returns
        -------
        xarray.DataArray
            Maximum daily maximum wind speed.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.sfcWindmax_max
        """
        params = _clean_up_params(params=params, func=self.func)
        return self.func(**params)
