import dask  # noqa
import numpy as np
import xarray as xr
import xclim as xc
from xclim.core.calendar import percentile_doy, resample_doy
from xclim.core.units import convert_units_to, rate2amount
from xclim.indices.generic import compare


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


def _get_percentile(da, perc, base_period_time_range):
    if isinstance(perc, xr.Dataset):
        return perc["per"]
    elif isinstance(perc, xr.DataArray):
        return perc
    tslice = slice(base_period_time_range[0], base_period_time_range[1])
    base_period = da.sel(time=tslice)
    with dask.config.set(**{"array.slicing.split_large_chunks": False}):
        per_doy = percentile_doy(base_period, per=perc)
        per_doy_comp = per_doy.compute()
    return per_doy_comp.sel(percentiles=perc)


def _convert_prsn_to_mm_day(da):
    da = convert_units_to(da, "kg/(m**2*day)", context="hydro")
    da.attrs["units"] = "kg/m**2"
    snd = xc.land.snw_to_snd(snw=da)
    da = convert_units_to(snd, "mm")
    da.attrs["units"] = "mm/day"
    da = da.rename("prsn")
    return da


BASE_PERIOD = ["1971-01-01", "2000-12-31"]


class CD:
    """Number of cold and dry days (tas, pr)."""

    base_period_time_range = BASE_PERIOD
    perc_tas = None
    perc_pr = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc_tas=perc_tas,
        perc_pr=perc_pr,
        **params,
    ):
        """Calculate number of cold and dry days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#cold_and_dry_days

        Returns
        -------
        Number of days where cold and dry conditions coincide.
        """
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if perc_tas is None:
            perc_tas = _get_percentile(
                da=da_tas,
                perc=25,
                base_period_time_range=base_period_time_range,
            )
        if perc_pr is None:
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            perc_pr = _get_percentile(
                da=da_pr_f,
                perc=25,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.cold_and_dry_days(
                tas_per=perc_tas,
                pr_per=perc_pr,
                **params,
            )


class CDD:
    """Maximum consecutive dry days (pr)."""

    thresh = 0.1

    def compute(thresh=thresh, **params):
        """Calculate maximum consecutive dry days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_dry_days

        Returns
        -------
        xarray.DataArray
            Maximum consecutive dry days.
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

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#consecutive_frost_days

        Returns
        -------
        Maximum number of consecutive frost days (tasmin < 0 degC).
        """
        return xc.atmos.consecutive_frost_days(**params)


class CHDYYx:
    """Maximum number of consecutive heat days (tasmax)."""

    thresh = 30

    def compute(thresh=thresh, **params):
        """Calculate maximum number of consecutive heat days.

        Parameters
        ----------
        https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_warm_days

        Returns
        -------
        Maximum number of consecutive heat days (tasmax > 30 degC).
        """
        return xc.atmos.maximum_consecutive_warm_days(**params)


class CSDI:
    """Cold spell duration index (tasmin)."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate cold spell duration index.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#cold_spell_duration_index

        Returns
        -------
        Number of days part of a 10th percentile cold spell.
        At least 6 consecutive days.
        """
        da = _get_da(params, "tasmin")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.cold_spell_duration_index(
                tasmin_per=perc,
                window=6,
                **params,
            )


class CSU:
    """Maximum consecutive summer days (tasmax)."""

    thresh = 25

    def compute(thresh=thresh, **params):
        """Calculate maximum consecutive summer days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_warm_days
        Returns
        -------
        xarray.DataArray
            Maximum consecutive summer days.
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.maximum_consecutive_warm_days(
            thresh=thresh,
            **params,
        )


class CW:
    """Number of cold and wet days (tas, pr)."""

    base_period_time_range = BASE_PERIOD
    perc_tas = None
    perc_pr = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc_tas=perc_tas,
        perc_pr=perc_pr,
        **params,
    ):
        """Calculate number of cold and wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#cold_and_wet_days

        Returns
        -------
        Number of days where cold and wet conditions coincide.
        """
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if perc_tas is None:
            perc_tas = _get_percentile(
                da=da_tas,
                perc=25,
                base_period_time_range=base_period_time_range,
            )
        if perc_pr is None:
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            perc_pr = _get_percentile(
                da=da_pr_f,
                perc=75,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.cold_and_wet_days(
                tas_per=perc_tas,
                pr_per=perc_pr,
                **params,
            )


class CWD:
    """Consecutive wet days (pr)."""

    thresh = 0.1

    def compute(thresh=thresh, **params):
        """Calculate maximum consecutive wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_wet_days

        Returns
        -------
        xarray.DataArray
            Maximum consecutive wet days.
        """
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.maximum_consecutive_wet_days(
            thresh=thresh,
            **params,
        )


class DD:
    """Number of dry days (pr)."""

    thresh = 0.1

    def compute(thresh=thresh, **params):
        """Calculate number of dry days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#dry_days

        Returns
        -------
        xarray.DataArray
            Number of dry days.
        """
        thresh = _thresh_string(thresh, "mm/day")
        return xc.atmos.dry_days(
            thresh=thresh,
            **params,
        )


class DSP:
    """Number of dry spells of minimum {window} days (pr)."""

    window = 5

    def compute(window=window, **params):
        """Calculate number of dry spells of minimum {window} days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#dry_spell_frequency

        Returns
        -------
        xarray.DataArray
            Number of dry periods of minimum {window} days.
        """
        return xc.atmos.dry_spell_frequency(window=window, **params)


class DTR:
    """Mean temperature rnage (tasmax, tasmin)."""

    def compute(**params):
        """Calculate mean of daily temperature range.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#daily_temperature_range

        Returns
        -------
        Mean of daily temperature range.
        """
        return xc.atmos.daily_temperature_range(**params)


class FD:
    """Number of frost days (tasmin)."""

    def compute(**params):
        """Calculate number of frost days (tasmin < 0.0 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#frost_days

        Returns
        -------
        xarray.DataArray
            Number of frost days (tasmin < 0.0 degC).
        """
        return xc.atmos.frost_days(**params)


class ID:
    """Number of ice days (tasmax)."""

    def compute(**params):
        """Calculate number of ice days (tasmax < 0.0 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#ice_days

        Returns
        -------
        xarray.DataArray
            Number of ice days (tasmax < 0.0 degC).
        """
        return xc.atmos.ice_days(**params)


class GD:
    """Number of growing degree days (tas)."""

    thresh = 4

    def compute(thresh=thresh, **params):
        """Calculate number of growing degree days (tas > 4 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#growing_degree_days
        Returns
        -------
        xarray.DataArray
            Number of growing degree days (tas > 4 degC).
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.growing_degree_days(
            thresh=thresh,
            **params,
        )


class GDYYx:
    """Number of consecutive growing degree day (tas)."""

    thresh = 4

    def compute(thresh=thresh, **params):
        """Calculate number of consecutive growing degree days (tas > 4 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#growing_season_length
        Returns
        -------
        xarray.DataArray
            Maximum number of consecutive growing degree days (tas > 4 degC).
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.growing_season_length(
            thresh=thresh,
            **params,
        )


class HD17:
    """Number of heating degree days (tas)."""

    def compute(**params):
        """Calculate number of heating degree days (tas < 17 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#heating_degree_days
        Returns
        -------
        xarray.DataArray
            Number of growing degree days (tas > 17 degC).
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#wet_precip_accumulation

        Returns
        -------
        Total precipitation amount of wet days (precip >= {thresh} mm)
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

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.precip_accumulation

        Returns
        -------
        xarray.DataArray
            Total precipitation.
        """
        return xc.atmos.precip_accumulation(**params)


class RRm:
    """Mean daily precipitation (pr)."""

    def compute(**params):
        """Calculate mean daily precipitation.

        Parameters
        ----------

        Returns
        -------
        xarray.DataArray
            Mean daily precipitation.
        """
        da = _get_da(params, "pr")
        pram = rate2amount(da)
        return (
            pram.resample(time=params["freq"])
            .mean(dim="time")
            .assign_attrs(units=pram.units)
        )


class RR1:
    """Number of wet days (pr)."""

    def compute(**params):
        """Calculate number of wet days (pr >= 1 mm/day).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#wetdays

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 1 mm/day).
        """
        return xc.atmos.wetdays(
            thresh="1 mm/day",
            **params,
        )


class R10mm:
    """Number of heavy precipitaiotn days (pr)."""

    def compute(**params):
        """Calculate number of wet days (pr >= 10 mm/day).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#wetdays

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 10 mm/day).
        """
        return xc.atmos.wetdays(
            thresh="10 mm/day",
            **params,
        )


class R20mm:
    """Number of very heavy precipitaiotn days (pr)."""

    def compute(**params):
        """Calculate number of wet days (pr >= 20 mm/day).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#wetdays

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 20 mm/day).
        """
        return xc.atmos.wetdays(
            thresh="20 mm/day",
            **params,
        )


class R25mm:
    """Number of super heavy precipitaiotn days (pr)."""

    def compute(**params):
        """Calculate number of wet days (pr >= 25 mm/day).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#wetdays

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 25 mm/day).
        """
        return xc.atmos.wetdays(
            thresh="25 mm/day",
            **params,
        )


class RRYYp:
    """Precip percentil value (pr)."""

    perc = 75
    base_period_time_range = BASE_PERIOD

    def compute(
        perc=perc,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate precip percentile value.

        Parameters
        ----------

        Returns
        -------
        xarray.DataArray
            Precip percentil value.
        """
        da = _get_da(params, "pr")
        da = _filter_out_small_values(da, "1 mm/day", context="hydro")
        return _get_percentile(
            da=da,
            perc=perc,
            base_period_time_range=base_period_time_range,
        )


class RYYp:
    """Number of wet days with precip over a given percentile (pr)."""

    perc = 75
    base_period_time_range = BASE_PERIOD

    def compute(
        perc=perc,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate number of wet days with precip over a given percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#days_over_precip_doy_thresh

        Returns
        -------
        xarray.DataArray
            Number of wet days over a given percentile.
        """
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, "1 mm/day", context="hydro")
        percentile = _get_percentile(
            da=da_pr,
            perc=perc,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.days_over_precip_doy_thresh(
            pr_per=percentile,
            **params,
        )


class RYYmm:
    """Number of days with precip over {tresh} (pr)."""

    thresh = 25

    def compute(thresh=thresh, **params):
        """Calculate number of wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#wetdays

        Returns
        -------
        xarray.DataArray
            Number of wet days.
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

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#max_1day_precipitation_amount

        Returns
        -------
        xarray.DataArray
            Maximum 1-day total precipitation.
        """
        return xc.atmos.max_1day_precipitation_amount(**params)


class RXYYday:
    """Maximum {window}-day total precipitation (pr)."""

    thresh = 5

    def compute(thresh=thresh, **params):
        """Calculate maximum {window}-day total precipitation.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#max_n_day_precipitation_amount

        Returns
        -------
        xarray.DataArray
            Maximum {window}-day total precipitation.
        """
        return xc.atmos.max_n_day_precipitation_amount(
            window=thresh,
            **params,
        )


class RYYpABS:
    """Total precipitation amount with precip > {perc}th percentile (pr)."""

    perc = 75
    base_period_time_range = BASE_PERIOD

    def compute(
        perc=perc,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate total precipitation amount
        with precip > {perc}th percentile.

        Parameters
        ----------

        Returns
        -------
        xarray.DataArray
            Precipitation fraction with precip > {perc}th percentile.
        """
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, "1 mm/day", context="hydro")
        pr_per = _get_percentile(
            da=da_pr,
            perc=perc,
            base_period_time_range=base_period_time_range,
        )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            pr_per = convert_units_to(pr_per, da, context="hydro")
            thresh = convert_units_to("1 mm/day", da, context="hydro")

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
    """Precipitation fraction with precip > {perc}th percentile (pr)."""

    perc = 75
    base_period_time_range = BASE_PERIOD

    def compute(
        perc=perc,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate precipitation fraction with precip > {perc}th percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#fraction_over_precip_thresh

        Returns
        -------
        xarray.DataArray
            Precipitation fraction with precip > {perc}th percentile.
        """
        da = _get_da(params, "pr")
        da_pr = _filter_out_small_values(da, "1 mm/day", context="hydro")
        percentile = _get_percentile(
            da=da_pr,
            perc=perc,
            base_period_time_range=base_period_time_range,
        )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.fraction_over_precip_thresh(
                pr_per=percentile,
                **params,
            )


class SDII:
    """Average precipitation during wet days (pr)."""

    def compute(**params):
        """Calculate average precipitation during wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.daily_pr_intensity

        Returns
        -------
        xarray.DataArray
            Average precipitation during wet days.
        """
        return xc.atmos.daily_pr_intensity(**params)


class SU:
    """Number of summer days (tasmax)."""

    thresh = 25

    def compute(thresh=thresh, **params):
        """Calculate number of summer days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tx_days_above

        Returns
        -------
        xarray.DataArray
            Number of summer days.
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tn_days_above

        Returns
        -------
        xarray.DataArray
            Number of uncomfortable sleep events.
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

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tg_mean

        Returns
        -------
        xarray.DataArray
            Mean daily mean temperature.
        """
        return xc.atmos.tg_mean(**params)


class TG10p:
    """Fraction of days with mean temperature < 10th percentile (tas)."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate fraction of days with mean temperature < 10th percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tg10p

        Returns
        -------
        xarray.DataArray
            Fraction of days with mean temperature < 10th percentile".
        """
        da = _get_da(params, "tas")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tg10p(
                tas_per=perc,
                **params,
            )


class TG90p:
    """Fraction of days with mean temperature > 90th percentile (tas)."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate fraction of days with mean temperature > 90th percentile".

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tg90p

        Returns
        -------
        xarray.DataArray
            Fraction of days with mean temperature > 90th percentile".
        """
        da = _get_da(params, "tas")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tg90p(
                tas_per=perc,
                **params,
            )


class TR:
    """Number of tropical nights (tasmin)."""

    thresh = 20

    def compute(thresh=thresh, **params):
        """Calculate number of tropical nights.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tn_days_above

        Returns
        -------
        xarray.DataArray
            Number of tropical nights.
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

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tx_mean

        Returns
        -------
        xarray.DataArray
            Mean daily maximum temperature.
        """
        return xc.atmos.tx_mean(**params)


class TX10p:
    """Fraction of days with max temperature < 10th percentile (tasmax)."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate fraction of days with max temperature < 10th percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tx10p

        Returns
        -------
        xarray.DataArray
            Fraction of days with maximum temperature < 10th percentile".
        """
        da = _get_da(params, "tasmax")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tx10p(
                tasmax_per=perc,
                **params,
            )


class TX90p:
    """Fraction of days with max temperature > 90th percentile (tasmax)."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate fraction of days with max temperature > 90th percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tx90p

        Returns
        -------
        xarray.DataArray
            Fraction of days with maximum temperature > 90th percentile".
        """
        da = _get_da(params, "tasmax")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tx90p(
                tasmax_per=perc,
                **params,
            )


class TXn:
    """Minimum maximum temperature (tasmax)."""

    def compute(**params):
        """Calculate minimum daily maximum temperature.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tx_min

        Returns
        -------
        xarray.DataArray
            Minimum daily maximum temperature.
        """
        return xc.atmos.tx_min(**params)


class TXx:
    """Maximum maximum temperature (tasmax)."""

    def compute(**params):
        """Calculate maximum daily maximum temperature.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tx_max

        Returns
        -------
        xarray.DataArray
            Maximum daily maximum temperature.
        """
        return xc.atmos.tx_max(**params)


class TN:
    """Mean minimum temperature (tasmin)."""

    def compute(**params):
        """Calculate mean daily minimum temperature.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tn_mean

        Returns
        -------
        xarray.DataArray
            Mean daily minimum temperature.
        """
        return xc.atmos.tn_mean(**params)


class TN10p:
    """Fraction of days with min temperature < 10th percentile."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate fraction of days with min temperature < 10th percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tn10p

        Returns
        -------
        xarray.DataArray
            Fraction of days with minimum temperature < 10th percentile".
        """
        da = _get_da(params, "tasmin")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=10,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tn10p(
                tasmin_per=perc,
                **params,
            )


class TN90p:
    """Fraction of days with min temperature > 90th percentile."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate fraction of days with min temperature > 90th percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tx90p

        Returns
        -------
        xarray.DataArray
            Fraction of days with minimum temperature > 90th percentile".
        """
        da = _get_da(params, "tasmin")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.tn90p(
                tasmin_per=perc,
                **params,
            )


class TNn:
    """Minimum minimum temperature (tasmin)."""

    def compute(**params):
        """Calculate minimum daily minimum temperature.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tn_min

        Returns
        -------
        xarray.DataArray
            Minimum daily minimum temperature.
        """
        return xc.atmos.tn_min(**params)


class TNx:
    """Maximum minimum temperature (tasmin)."""

    def compute(**params):
        """Calculate maximum daily minimum temperature.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tn_max

        Returns
        -------
        xarray.DataArray
            Maximum daily minimum temperature.
        """
        return xc.atmos.tn_max(**params)


class WD:
    """Number of warm and dry days (tas, pr)."""

    base_period_time_range = BASE_PERIOD
    perc_tas = None
    perc_pr = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc_tas=perc_tas,
        perc_pr=perc_pr,
        **params,
    ):
        """Calculate number of warm and dry days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#warm_and_dry_days

        Returns
        -------
        Number of days where warm and dry conditions coincide.
        """
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if perc_tas is None:
            perc_tas = _get_percentile(
                da=da_tas,
                perc=75,
                base_period_time_range=base_period_time_range,
            )
        if perc_pr is None:
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            perc_pr = _get_percentile(
                da=da_pr_f,
                perc=25,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.warm_and_dry_days(
                tas_per=perc_tas,
                pr_per=perc_pr,
                **params,
            )


class WSDI:
    """Warm spell duration index (tasmax)."""

    base_period_time_range = BASE_PERIOD
    perc = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc=perc,
        **params,
    ):
        """Calculate warm spell duration index.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#warm_spell_duration_index

        Returns
        -------
        Number of days part of a 90th percentile warm spell.
        At least 6 consecutive days.
        """
        da = _get_da(params, "tasmax")
        if perc is None:
            perc = _get_percentile(
                da=da,
                perc=90,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.warm_spell_duration_index(
                tasmax_per=perc,
                window=6,
                **params,
            )


class WW:
    """Number of warm and wet days (tas, pr)."""

    base_period_time_range = BASE_PERIOD
    perc_tas = None
    perc_pr = None

    def compute(
        base_period_time_range=base_period_time_range,
        perc_tas=perc_tas,
        perc_pr=perc_pr,
        **params,
    ):
        """Calculate number of warm and wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#warm_and_wet_days

        Returns
        -------
        Number of days where warm and wet conditions coincide.
        """
        da_tas = _get_da(params, "tas")
        da_pr = _get_da(params, "pr")
        if perc_tas is None:
            perc_tas = _get_percentile(
                da=da_tas,
                perc=75,
                base_period_time_range=base_period_time_range,
            )
        if perc_pr is None:
            da_pr_f = _filter_out_small_values(
                da_pr,
                "1 mm/day",
                context="hydro",
            )
            perc_pr = _get_percentile(
                da=da_pr_f,
                perc=75,
                base_period_time_range=base_period_time_range,
            )
        with dask.config.set(**{"array.slicing.split_large_chunks": False}):
            return xc.atmos.warm_and_wet_days(
                tas_per=perc_tas,
                pr_per=perc_pr,
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#cold_spell_frequency

        Returns
        -------
        Number of cold spells of at least {window} consecutive days
        with temperature below {thresh}.
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.cold_spell_frequency(
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#hot_spell_frequency

        Returns
        -------
        Number of hot spells of at least {window} consecutive days
        with maximum temperature above {thresh}.
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.hot_spell_frequency(
            thresh_tasmax=thresh,
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#hot_spell_max_length

        Returns
        -------
        Maximum length of hot spells of at least {window} consecutive days
        with maximum temperature above {thresh}.
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.hot_spell_max_length(
            thresh_tasmax=thresh,
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#days_with_snow

        Returns
        -------
        Number of days with solid precipitation flux above {thresh} threshold.
        """
        thresh = _thresh_string(thresh, "mm/day")
        da = _get_da(params, "prsn")
        da = _convert_prsn_to_mm_day(da)
        if "ds" in params.keys():
            del params["ds"]
        params["prsn"] = da
        return xc.atmos.days_with_snow(
            low=thresh,
            **params,
        )


class SCD:
    """Snow cover duration."""

    thresh = 1

    def compute(thresh=thresh, **params):
        """Calculate snow cover duration.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#snow_cover_duration

        Returns
        -------
        Number of days with snow cover above {thresh} threshold.
        """
        thresh = _thresh_string(thresh, "cm")
        return xc.land.snd_season_length(
            thresh=thresh,
            **params,
        )


class Sint:
    """Snowfall intensity."""

    def compute(**params):
        """Calculate snowfall intensity.

        Parameters
        ----------

        Returns
        -------
        Mean daily snowfall during days with snowfall > 1mm/day
        """

        da = _get_da(params, "prsn")
        da = _convert_prsn_to_mm_day(da)
        if "ds" in params.keys():
            del params["ds"]
        params["prsn"] = da
        masked = xr.where(da > 1, da, np.nan)
        mean = masked.resample(time=params["freq"]).mean(dim="time")
        return xr.where(mean == np.nan, 0, mean)


class Sfreq:
    """Snowfall frequency."""

    def compute(**params):
        """Calculate snowfall frequency.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#days_with_snow

        Returns
        -------
        Percentage of days with snowfall > 1mm/day.
        """
        thresh = _thresh_string(1, "mm/day")
        da = _get_da(params, "prsn")
        da = _convert_prsn_to_mm_day(da)
        if "ds" in params.keys():
            del params["ds"]
        params["prsn"] = da
        sd = xc.atmos.days_with_snow(
            low=thresh,
            **params,
        )
        ndays = da.resample(time=params["freq"]).count(dim="time")
        sfreq = sd / ndays * 100
        return sfreq.assign_attrs(**sd.attrs)


class UTCI:
    """Universal thermal climate index."""

    stat = "average"
    mask_invalid = True

    def compute(stat=stat, mask_invalid=mask_invalid, **params):
        """Calculate universal thermal climate index.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#universal_thermal_cliamte_index

        Returns
        -------
        Universal Thermal Climate Index.
        """
        return xc.atmos.universal_thermal_climate_index(
            stat=stat,
            mask_invalid=mask_invalid,
            **params,
        )


class WI:
    """Number of winter days (tas)."""

    thresh = -10

    def compute(thresh=thresh, **params):
        """Calculate number of winter days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tg_days_below

        Returns
        -------
        xarray.DataArray
            Number of winter days.
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.tg_days_below(
            thresh=thresh,
            **params,
        )


class HW:
    """Maximum length of heat waves (tasmax, tasmin)."""

    thresh_tasmin = 22
    thresh_tasmax = 30

    def compute(
        thresh_tasmax=thresh_tasmax,
        thresh_tasmin=thresh_tasmin,
        **params,
    ):
        """Calculate maximum number of heat waves.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#heat_wave_max_length

        Returns
        -------
        xarray.DataArray
            Maximum length of heat waves.
        """
        thresh_tasmax = _thresh_string(thresh_tasmax, "degC")
        thresh_tasmin = _thresh_string(thresh_tasmin, "degC")
        return xc.atmos.heat_wave_max_length(
            thresh_tasmax=thresh_tasmax,
            thresh_tasmin=thresh_tasmin,
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#growing_season_start

        Returns
        -------
        xarray.DataArray
            Growing season start.
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#growing_season_end

        Returns
        -------
        xarray.DataArray
            Growing season end.
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#frost_free_season_start

        Returns
        -------
        xarray.DataArray
            Frost free season start.
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
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#frost_free_season_end

        Returns
        -------
        xarray.DataArray
            Frost free season end.
        """
        thresh = _thresh_string(thresh, "degC")
        return xc.atmos.frost_free_season_end(
            thresh=thresh,
            window=window,
            **params,
        )
