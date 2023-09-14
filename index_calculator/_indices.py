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


class CD:
    """Number of cold and dry days (tas, pr)."""

    tas_per = None
    pr_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tas_per=tas_per,
        pr_per=pr_per,
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
        base_period_time_range: list
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
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if tas_per is None:
            tas_per = _get_percentile(
                da=da_tas,
                per=25,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
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
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.cold_and_dry_days(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class CDD:
    """Maximum consecutive dry days (pr)."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate maximum consecutive dry days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.maximum_consecutive_dry_days(
            thresh=thresh,
            **params,
        )


class CFD:
    """Maximum number of consecutive frost days (tasmin)."""

    def compute(**params):
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
        return xc.atmos.consecutive_frost_days(**params)


class CHDYYx:
    """Maximum number of consecutive heat days (tasmax)."""

    thresh = 30

    def compute(thresh=thresh, **params):
        """Calculate maximum number of consecutive heat days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.maximum_consecutive_warm_days(
            thresh=thresh,
            **params,
        )


class CSDI:
    """Cold spell duration index (tasmin)."""

    window = 6
    tasmin_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        window=window,
        base_period_time_range=base_period_time_range,
        tasmin_per=tasmin_per,
        **params,
    ):
        """Calculate cold spell duration index.

        Parameters
        ----------
        window: int
            Minimum number of days with temperature below `tasmin_per`
            to qualify as a cold spell (default: 6).
        tasmin_per: xr.DataArray, optional
            Minimum temperature 10th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tasmin")
        if tasmin_per is None:
            tasmin_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.cold_spell_duration_index(
                tasmin_per=tasmin_per,
                window=window,
                **params,
            )


class CSU:
    """Maximum consecutive summer days (tasmax)."""

    thresh = 25

    def compute(thresh=thresh, **params):
        """Calculate maximum consecutive summer days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.maximum_consecutive_warm_days(
            thresh=thresh,
            **params,
        )


class CW:
    """Number of cold and wet days (tas, pr)."""

    tas_per = None
    pr_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tas_per=tas_per,
        pr_per=pr_per,
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
        base_period_time_range: list
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
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if tas_per is None:
            tas_per = _get_percentile(
                da=da_tas,
                per=25,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
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
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.cold_and_wet_days(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class CWD:
    """Consecutive wet days (pr)."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate maximum consecutive wet days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.maximum_consecutive_wet_days(
            thresh=thresh,
            **params,
        )


class DD:
    """Number of dry days (pr)."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate number of dry days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.dry_days(
            thresh=thresh,
            **params,
        )


class DSf:
    """Number of dry spells (pr)."""

    thresh = 1
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate number of dry spells.

        Parameters
        ----------
        thresh: int or string
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int
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
        thresh = _thresh_string(thresh, "mm")
        return xc.atmos.dry_spell_frequency(
            thresh=thresh,
            window=window,
            **params,
        )


class DSx:
    """Maximum length of dry spells (pr)."""

    thresh = 1
    window = 1

    def compute(thresh=thresh, window=window, **params):
        """Calculate maximum length of dry spells.

        Parameters
        ----------
        thresh: int or string
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int
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
        thresh = _thresh_string(thresh, "mm")
        return xc.atmos.dry_spell_max_length(
            thresh=thresh,
            window=window,
            **params,
        )


class DSn:
    """Total number of days in dry spells (pr)."""

    thresh = 1
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate total number of days in dry spells.

        Parameters
        ----------
        thresh: int or string
            Threshold precipitation below which a day is considered
            as a dry day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int
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
        thresh = _thresh_string(thresh, "mm")
        return xc.atmos.dry_spell_total_length(
            thresh=thresh,
            window=window,
            **params,
        )


class WSf:
    """Number of wet spells (pr)."""

    thresh = 1
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate number of wet spells.

        Parameters
        ----------
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int
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
        thresh = _thresh_string(thresh, "mm")
        return xc.atmos.wet_spell_frequency(
            thresh=thresh,
            window=window,
            **params,
        )


class WSx:
    """Maximum length of wet spells (pr)."""

    thresh = 1
    window = 1

    def compute(thresh=thresh, window=window, **params):
        """Calculate maximum length of wet spells.

        Parameters
        ----------
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int
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
        thresh = _thresh_string(thresh, "mm")
        return xc.atmos.wet_spell_max_length(
            thresh=thresh,
            window=window,
            **params,
        )


class WSn:
    """Total number of days in wet spells (pr)."""

    thresh = 1
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate total number of days in wet spells.

        Parameters
        ----------
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm).
            If type of threshold is an integer the unit is set to mm.
        window: int
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
        thresh = _thresh_string(thresh, "mm")
        return xc.atmos.wet_spell_total_length(
            thresh=thresh,
            window=window,
            **params,
        )


class DTR:
    """Mean temperature rnage (tasmax, tasmin)."""

    def compute(**params):
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
        return xc.atmos.daily_temperature_range(**params)


class FD:
    """Number of frost days (tasmin)."""

    def compute(**params):
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
        return xc.atmos.frost_days(**params)


class LFD:
    """Number of late frost days (tasmin)."""

    start_date = "04-01"
    end_date = "06-30"

    def compute(start_date=start_date, end_date=end_date, **params):
        """Calculate number of late frost days (tasmin < 0.0 degC).

        Parameters
        ----------
        start_date: str
            Left bound of the period to be considered.
        end_date: str
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
        return xc.atmos.late_frost_days(
            date_bounds=(start_date, end_date),
            **params,
        )


class ID:
    """Number of ice days (tasmax)."""

    def compute(**params):
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
        return xc.atmos.ice_days(**params)


class GD:
    """Cumulative growing degree days (tas)."""

    thresh = 4

    def compute(thresh=thresh, **params):
        """Calculate cumulative growing degree days (tas > thresh).

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.growing_degree_days(
            thresh=thresh,
            **params,
        )


class HD17:
    """Cumulative heating degree days (tas)."""

    def compute(**params):
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
        return xc.atmos.heating_degree_days(
            **params,
        )


class PRCPTOT:
    """Total precipitation amount (pr)."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate total precipitation amount.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.wet_precip_accumulation(
            thresh=thresh,
            **params,
        )


class RR:
    """Total precipitation (pr)."""

    def compute(**params):
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
        return xc.atmos.precip_accumulation(**params)


class RRm:
    """Mean daily precipitation (pr)."""

    def compute(**params):
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
        return xc.atmos.precip_average(**params)


class RR1:
    """Number of wet days (pr)."""

    def compute(**params):
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
        return xc.atmos.wetdays(
            thresh="1 mm/day",
            **params,
        )


class R10mm:
    """Number of heavy precipitation days (pr)."""

    def compute(**params):
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
        return xc.atmos.wetdays(
            thresh="10 mm/day",
            **params,
        )


class R20mm:
    """Number of very heavy precipitation days (pr)."""

    def compute(**params):
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
        return xc.atmos.wetdays(
            thresh="20 mm/day",
            **params,
        )


class R25mm:
    """Number of super heavy precipitation days (pr)."""

    def compute(**params):
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
        return xc.atmos.wetdays(
            thresh="25 mm/day",
            **params,
        )


class RRYYp:
    """Precip percentil value for wet days (pr)."""

    per = 75
    thresh = 1
    base_period_time_range = BASE_PERIOD

    def compute(
        per=per,
        thresh=thresh,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate precip percentile reference value
        for wet days (pr > thresh).

        Parameters
        ----------
        per: int
            Percentile value.
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list
            List with left bound is start year string and right bound
            is end year string for calculating the precip percentile
            reference value.

        Returns
        -------
        xarray.DataArray
            Precip {per}th percentil reference value
            for wet days (pr > {thresh}).
        """
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da = _filter_out_small_values(da, thresh, context="hydro")
        return _get_percentile(
            da=da,
            per=per,
            base_period_time_range=base_period_time_range,
        )


class RYYp:
    """Number of wet days with precip over a given percentile (pr)."""

    per = 75
    thresh = 1
    base_period_time_range = BASE_PERIOD

    def compute(
        per=per,
        thresh=thresh,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate number of wet days (pr > thresh)
        with precip over a given percentile.

        Parameters
        ----------
        per: int
            Precipitation percentile value.
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list
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
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, thresh, context="hydro")
        pr_per = _get_percentile(
            da=da_pr,
            per=per,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.days_over_precip_doy_thresh(
            pr_per=pr_per,
            **params,
        )


class RYYmm:
    """Number of days with precip over threshold (pr)."""

    thresh = 25

    def compute(thresh=thresh, **params):
        """Calculate number of wet days.

        Parameters
        ----------
        thresh:
        Threshold precipitation above which a day is considered
            as a wet day(default: 25 mm/day).
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.wetdays(
            thresh=thresh,
            **params,
        )


class RX1day:
    """Maximum 1-day total precipitation (pr)."""

    def compute(**params):
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
        return xc.atmos.max_1day_precipitation_amount(**params)


class RXYYday:
    """Maximum n-day total precipitation (pr)."""

    window = 5

    def compute(window=window, **params):
        """Calculate maximum {window}-day total precipitation.

        Parameters
        ----------
        window: int
            Window size in days.

        Returns
        -------
        xarray.DataArray
            Maximum {window}-day total precipitation.

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.max_n_day_precipitation_amount
        """
        return xc.atmos.max_n_day_precipitation_amount(
            window=window,
            **params,
        )


class RYYpABS:
    """Total precipitation amount with precip above percentile
    on wet days (pr)."""

    per = 75
    thresh = 1
    base_period_time_range = BASE_PERIOD

    def compute(
        per=per,
        thresh=thresh,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate total precipitation amount with
        precip > {perc}th percentile on wet days (pr > thresh).

        Parameters
        ----------
        per: int
            Percentile value.
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list
            List with left bound is start year string and right bound
            is end year string for calulating the precip percentile
            reference value.

        Returns
        -------
        xarray.DataArray
            Precipitation fraction with precip > {perc}th percentile
            on wet days (pr > {thresh}).
        """
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

    per = 75
    thresh = 1
    base_period_time_range = BASE_PERIOD

    def compute(
        per=per,
        thresh=thresh,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate precipitation fraction with precip above percentile
        on wet days (pr > thresh).

        Parameters
        ----------
        per: int
            Percentile value.
        thresh: int or string
            Threshold precipitation above which a day is considered
            as a wet day (default: 1 mm/day).
            If type of threshold is an integer the unit is set to mm/day.
        base_period_time_range: list
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
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, thresh, context="hydro")
        pr_per = _get_percentile(
            da=da_pr,
            per=per,
            base_period_time_range=base_period_time_range,
        )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.fraction_over_precip_thresh(
                pr_per=pr_per,
                **params,
            )


class SDII:
    """Average precipitation during wet days (pr)."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate average precipitation during wet days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(1, "mm/day")
        return xc.atmos.daily_pr_intensity(
            thresh=thresh,
            **params,
        )


class SU:
    """Number of summer days (tasmax)."""

    thresh = 25

    def compute(thresh=thresh, **params):
        """Calculate number of summer days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.tx_days_above(
            thresh=thresh,
            **params,
        )


class SQI:
    """Number of uncomfortable sleep events (tasmin)."""

    thresh = 18

    def compute(thresh=thresh, **params):
        """Calculate number of uncomfortable sleep events.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.tn_days_above(
            thresh=thresh,
            **params,
        )


class TG:
    """Mean mean temperature (tas)."""

    def compute(**params):
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
        return xc.atmos.tg_mean(**params)


class TG10p:
    """Fraction of days with mean temperature < 10th percentile (tas)."""

    tas_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tas_per=tas_per,
        **params,
    ):
        """Calculate fraction of days with mean temperature < 10th percentile.

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Temperature 10th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tas")
        if tas_per is None:
            tas_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tg10p(
                tas_per=tas_per,
                **params,
            )


class TG90p:
    """Fraction of days with mean temperature > 90th percentile (tas)."""

    tas_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tas_per=tas_per,
        **params,
    ):
        """Calculate fraction of days with mean temperature > 90th percentile".

        Parameters
        ----------
        tas_per: xr.DataArray, optional
            Temperature 90th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tas")
        if tas_per is None:
            tas_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tg90p(
                tas_per=tas_per,
                **params,
            )


class TR:
    """Number of tropical nights (tasmin)."""

    thresh = 20

    def compute(thresh=thresh, **params):
        """Calculate number of tropical nights.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.tn_days_above(
            thresh=thresh,
            **params,
        )


class TX:
    """Mean maximum temperature (tasmax)."""

    def compute(**params):
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
        return xc.atmos.tx_mean(**params)


class TX10p:
    """Fraction of days with max temperature < 10th percentile (tasmax)."""

    tasmax_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tasmax_per=tasmax_per,
        **params,
    ):
        """Calculate fraction of days with max temperature < 10th percentile.

        Parameters
        ----------
        tasmax_per: xr.DataArray, optional
            Maximum temperature 10th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tasmax")
        if tasmax_per is None:
            tasmax_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tx10p(
                tasmax_per=tasmax_per,
                **params,
            )


class TX90p:
    """Fraction of days with max temperature > 90th percentile (tasmax)."""

    tasmax_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tasmax_per=tasmax_per,
        **params,
    ):
        """Calculate fraction of days with max temperature > 90th percentile.

        Parameters
        ----------
        tasmax_per: xr.DataArray, optional
            Maximum temperature 90th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tasmax")
        if tasmax_per is None:
            tasmax_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tx90p(
                tasmax_per=tasmax_per,
                **params,
            )


class TXn:
    """Minimum maximum temperature (tasmax)."""

    def compute(**params):
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
        return xc.atmos.tx_min(**params)


class TXx:
    """Maximum maximum temperature (tasmax)."""

    def compute(**params):
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
        return xc.atmos.tx_max(**params)


class TN:
    """Mean minimum temperature (tasmin)."""

    def compute(**params):
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
        return xc.atmos.tn_mean(**params)


class TN10p:
    """Fraction of days with min temperature < 10th percentile."""

    tasmin_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tasmin_per=tasmin_per,
        **params,
    ):
        """Calculate fraction of days with min temperature < 10th percentile.

        Parameters
        ----------
        tasmin_per: xr.DataArray, optional
            Minimum temperature 10th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tasmin")
        if tasmin_per is None:
            tasmin_per = _get_percentile(
                da=da,
                per=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tn10p(
                tasmin_per=tasmin_per,
                **params,
            )


class TN90p:
    """Fraction of days with min temperature > 90th percentile."""

    tasmin_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tasmin_per=tasmin_per,
        **params,
    ):
        """Calculate fraction of days with min temperature > 90th percentile.

        Parameters
        ----------
        tasmin_per: xr.DataArray, optional
            Minimum temperature 90th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tasmin")
        if tasmin_per is None:
            tasmin_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tn90p(
                tasmin_per=tasmin_per,
                **params,
            )


class TNn:
    """Minimum minimum temperature (tasmin)."""

    def compute(**params):
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
        return xc.atmos.tn_min(**params)


class TNx:
    """Maximum minimum temperature (tasmin)."""

    def compute(**params):
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
        return xc.atmos.tn_max(**params)


class WD:
    """Number of warm and dry days (tas, pr)."""

    tas_per = None
    pr_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tas_per=tas_per,
        pr_per=pr_per,
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
        base_period_time_range: list
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
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if tas_per is None:
            tas_per = _get_percentile(
                da=da_tas,
                per=75,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
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
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.warm_and_dry_days(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class WSDI:
    """Warm spell duration index (tasmax)."""

    window = 6
    tasmax_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        window=window,
        base_period_time_range=base_period_time_range,
        tasmax_per=tasmax_per,
        **params,
    ):
        """Calculate warm spell duration index.

        Parameters
        ----------
        window: int
            Minimum number of days with temperature above `tasmax_per`
            to qualify as a warm spell (default: 6).
        tasmin_per: xr.DataArray, optional
            Maximum temperature 90th percentile reference value.
        base_period_time_range: list
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
        da = _get_da(params, "tasmax")
        if tasmax_per is None:
            tasmax_per = _get_percentile(
                da=da,
                per=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.warm_spell_duration_index(
                tasmax_per=tasmax_per,
                window=window,
                **params,
            )


class WW:
    """Number of warm and wet days (tas, pr)."""

    tas_per = None
    pr_per = None
    base_period_time_range = BASE_PERIOD

    def compute(
        base_period_time_range=base_period_time_range,
        tas_per=tas_per,
        pr_per=pr_per,
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
        base_period_time_range: list
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
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if tas_per is None:
            tas_per = _get_percentile(
                da=da_tas,
                per=75,
                base_period_time_range=base_period_time_range,
            )
        if pr_per is None:
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
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.warm_and_wet_days(
                tas_per=tas_per,
                pr_per=pr_per,
                **params,
            )


class CSf:
    """Number of cold spells (tas)."""

    thresh = -10
    window = 3

    def compute(thresh=thresh, window=window, **params):
        """Calculate number of cold spells.

        Parameters
        ----------
        thresh: int or string
            Threshold temperature below which a day is considered
            as a cold day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.cold_spell_frequency(
            thresh=thresh,
            window=window,
            **params,
        )


class CSx:
    """Maximum length of cold spells (tas)."""

    thresh = -10
    window = 1

    def compute(thresh=thresh, window=window, **params):
        """Calculate maximum length of cold spells.

        Parameters
        ----------
        thresh: int or string
            Threshold temperature below which a day is considered
            as a cold day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.cold_spell_max_length(
            thresh=thresh,
            window=window,
            **params,
        )


class CSn:
    """Total number of days in cold spells (tas)."""

    thresh = -10
    window = 3

    def compute(thresh=thresh, window=window, **params):
        """Calculate total number of days in cold spells.

        Parameters
        ----------
        thresh: int or string
            Threshold temperature below which a day is considered
            as a cold day (default: -10 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.cold_spell_total_length(
            thresh=thresh,
            window=window,
            **params,
        )


class HSf:
    """Number of hot spells (tasmax)."""

    thresh = 35
    window = 3

    def compute(thresh=thresh, window=window, **params):
        """Calculate number of hot spells.

        Parameters
        ----------
        thresh: int or string
            Threshold maximum temperature above which a day is considered
            as a hot day (default: 35 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.hot_spell_frequency(
            thresh=thresh,
            window=window,
            **params,
        )


class HSx:
    """Maximum lenght of hot spells (tasmax)."""

    thresh = 35
    window = 1

    def compute(thresh=thresh, window=window, **params):
        """Calculate maximum lenght of hot spells.

        Parameters
        ----------
        thresh: int or string
            Threshold maximum temperature above which a day is considered
            as a hot day (default: 35 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.hot_spell_max_length(
            thresh=thresh,
            window=window,
            **params,
        )


class HSn:
    """Total number of days in hot spells (tasmax)."""

    thresh = 35
    window = 3

    def compute(thresh=thresh, window=window, **params):
        """Calculate total number of days in hot spells.

        Parameters
        ----------
        thresh: int or string
            Threshold maximum temperature above which a day is considered
            as a hot day (default: 35 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.hot_spell_total_length(
            thresh=thresh,
            window=window,
            **params,
        )


class SD:
    """Number of snow days."""

    thresh = 1

    def compute(thresh=thresh, **params):
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.days_with_snow(
            low=thresh,
            **params,
        )


class SCD:
    """Snow cover duration."""

    thresh = 3

    def compute(
        thresh=thresh,
        **params,
    ):
        """Calculate snow cover duration.

        Parameters
        ----------
        thresh: int or string
            Threshold snow thickness above which a day is considered
            as a snow day (default: 3 cm).
            If type of threshold is an integer the unit is set to cm.

        Returns
        -------
        xarray.DataArray
            Number of days with snow cover above {thresh} threshold.
        """
        thresh = _thresh_string(thresh, "cm")
        return xc.land.snd_season_length(
            thresh=thresh,
            **params,
        )


class Sint:
    """Snowfall intensity."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate snowfall intensity.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.snowfall_intensity(
            thresh=thresh,
            **params,
        )


class Sfreq:
    """Snowfall frequency."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate snowfall frequency.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.snowfall_frequency(
            thresh=thresh,
            **params,
        )


class UTCI:
    """Universal thermal climate index."""

    stat = "average"
    mask_invalid = True

    def compute(stat=stat, mask_invalid=mask_invalid, **params):
        """Calculate universal thermal climate index.

        Parameters
        ----------
        stat: {‘average’, ‘sunlit’, ‘instant’}
            Which statistic to apply. If “average”, the average of the cosine
            of the solar zenith angle is calculated.
            If “instant”, the instantaneous cosine of the solar zenith angle is
            calculated.
            If “sunlit”, the cosine of the solar zenith angle is calculated
            during the sunlit period of each interval.
            If “instant”, the instantaneous cosine of the solar zenith angle is
            calculated.
            This is necessary if mrt is not None (default: average).
        mask_valid: bool
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
        return xc.atmos.universal_thermal_climate_index(
            stat=stat,
            mask_invalid=mask_invalid,
            **params,
        )


class WI:
    """Number of winter days (tasmin)."""

    thresh = -10

    def compute(thresh=thresh, **params):
        """Calculate number of winter days.

        Parameters
        ----------
        thresh: int or string
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.tn_days_below(
            thresh=thresh,
            **params,
        )


class HWf:
    """Number of heat waves (tasmax, tasmin)."""

    thresh_tasmin = 22
    thresh_tasmax = 30
    window = 3

    def compute(
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        **params,
    ):
        """Calculate number of heat waves.

        Parameters
        ----------
        thresh_tasmin: int or string
            Threshold minimum temperature above which a day is considered
            as a heat day (default: 22 degC).
            If type of threshold is an integer the unit is set to degC.
        thresh_tasmax: int or string
            Threshold maximum temperature above which a day is considered
            as a winter day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")
        return xc.atmos.heat_wave_frequency(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
            window=window,
            **params,
        )


class HWx:
    """Maximum length of heat waves (tasmax, tasmin)."""

    thresh_tasmin = 22
    thresh_tasmax = 30
    window = 1

    def compute(
        thresh_tasmax=thresh_tasmax,
        thresh_tasmin=thresh_tasmin,
        window=window,
        **params,
    ):
        """Calculate maximum number of heat waves.

        Parameters
        ----------
        thresh_tasmin: int or string
            Threshold minimum temperature above which a day is considered
            as a heat day (default: 22 degC).
            If type of threshold is an integer the unit is set to degC.
        thresh_tasmax: int or string
            Threshold maximum temperature above which a day is considered
            as a winter day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")
        return xc.atmos.heat_wave_max_length(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
            window=window,
            **params,
        )


class HWn:
    """Total number of days in heat waves (tasmax, tasmin)."""

    thresh_tasmin = 22
    thresh_tasmax = 30
    window = 3

    def compute(
        thresh_tasmin=thresh_tasmin,
        thresh_tasmax=thresh_tasmax,
        window=window,
        **params,
    ):
        """Calculate total number of days in heat waves.

        Parameters
        ----------
        thresh_tasmin: int or string
            Threshold minimum temperature above which a day is considered
            as a heat day (default: 22 degC).
            If type of threshold is an integer the unit is set to degC.
        thresh_tasmax: int or string
            Threshold maximum temperature above which a day is considered
            as a winter day (default: 30 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")
        return xc.atmos.heat_wave_total_length(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
            window=window,
            **params,
        )


class GSS:
    """Growing season start (tas)."""

    thresh = 5
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate growing season start.

        Parameters
        ----------
        thresh: int or string
            Threshold temperature above which the growing season starts
            (default: 5 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.growing_season_start(
            thresh=thresh,
            window=window,
            **params,
        )


class GSE:
    """Growing season end (tas)."""

    thresh = 5
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate growing season end.

        Parameters
        ----------
        thresh: int or string
            Threshold temperature below which the growing season ends
            (default: 5 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.growing_season_end(
            thresh=thresh,
            window=window,
            **params,
        )


class FFS:
    """Frost free season start (tasmin)."""

    thresh = 0
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate frost free season start.

        Parameters
        ----------
        thresh: int or string
            Threshold minimum temperature above which the frost free season
            starts (default: 0 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.frost_free_season_start(
            thresh=thresh,
            window=window,
            **params,
        )


class FFE:
    """Frost free season end (tasmin)."""

    thresh = 0
    window = 5

    def compute(thresh=thresh, window=window, **params):
        """Calculate frost free season end.

        Parameters
        ----------
        thresh: int or string
            Threshold minimum temperature below which the frost free season
            ends (default: 0 degC).
            If type of threshold is an integer the unit is set to degC.
        window: int
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
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.frost_free_season_end(
            thresh=thresh,
            window=window,
            **params,
        )


class FG:
    """Mean daily mean wind speed."""

    def compute(**params):
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
        return xc.atmos.sfcWind_mean(**params)


class FGn:
    """Minimum daily mean wind speed."""

    def compute(**params):
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
        return xc.atmos.sfcWind_min(**params)


class FGx:
    """Maximum daily mean wind speed."""

    def compute(**params):
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
        return xc.atmos.sfcWind_max(**params)


class FX:
    """Mean daily maximum wind speed."""

    def compute(**params):
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
        return xc.atmos.sfcWindmax_mean(**params)


class FXn:
    """Minimum daily maximum wind speed."""

    def compute(**params):
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
        return xc.atmos.sfcWindmax_min(**params)


class FXx:
    """Maximum daily maximum wind speed."""

    def compute(**params):
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
        return xc.atmos.sfcWindmax_max(**params)
