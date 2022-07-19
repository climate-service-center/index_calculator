import dask  # noqa
import xclim as xc
from xclim.core.calendar import percentile_doy


def thresh_string(thresh, units):
    if isinstance(thresh, str):
        return thresh
    else:
        return "{} {}".format(str(thresh), units)


def get_da(dictionary, var):
    if "ds" in dictionary.keys():
        return dictionary["ds"][var]
    elif var in dictionary.keys():
        return dictionary[var]
    raise ValueError("Variable {} not found!")


def get_percentile(da, perc, base_period_time_range):
    tslice = slice(base_period_time_range[0], base_period_time_range[1])
    base_period = da.sel(time=tslice)
    per_doy = percentile_doy(base_period, per=perc)
    return per_doy.sel(percentiles=perc)


BASE_PERIOD = ["1951-01-01", "1955-12-31"]


class CD:

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate number of cold and dry days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#cold_and_dry_days

        Returns
        -------
        Number of days where cold and dry conditions coincide.
        """
        da_tas = get_da(params, "tas")
        da_pr = get_da(params, "pr")
        percentile_tas = get_percentile(
            da=da_tas,
            perc=25,
            base_period_time_range=base_period_time_range,
        )
        percentile_pr = get_percentile(
            da=da_pr,
            perc=25,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.cold_and_dry_days(
            tas_per=percentile_tas,
            pr_per=percentile_pr,
            **params,
        )


class CDD:
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
        thresh = thresh_string(thresh, "mm/day")
        return xc.atmos.maximum_consecutive_dry_days(
            thresh=thresh,
            **params,
        )


class CFD:
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

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
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
        da = get_da(params, "tasmin")
        percentile = get_percentile(
            da=da,
            perc=10,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.cold_spell_duration_index(
            tasmin_per=percentile,
            window=6,
            **params,
        )


class CSU:
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
        thresh = thresh_string(thresh, "degC")
        return xc.atmos.maximum_consecutive_warm_days(
            thresh=thresh,
            **params,
        )


class CW:

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate number of cold and wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#cold_and_wet_days

        Returns
        -------
        Number of days where cold and wet conditions coincide.
        """
        da_tas = get_da(params, "tas")
        da_pr = get_da(params, "pr")
        percentile_tas = get_percentile(
            da=da_tas,
            perc=25,
            base_period_time_range=base_period_time_range,
        )
        percentile_pr = get_percentile(
            da=da_pr,
            perc=75,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.cold_and_wet_days(
            tas_per=percentile_tas,
            pr_per=percentile_pr,
            **params,
        )


class CWD:
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
        thresh = thresh_string(thresh, "mm/day")
        return xc.atmos.maximum_consecutive_wet_days(
            thresh=thresh,
            **params,
        )


class DD:
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
        thresh = thresh_string(thresh, "mm/day")
        return xc.atmos.dry_days(
            thresh=thresh,
            **params,
        )


class DSP:
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
        thresh = thresh_string(thresh, "degC")
        return xc.atmos.growing_degree_days(
            thresh=thresh,
            **params,
        )


class GDYYx:

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
        thresh = thresh_string(thresh, "degC")
        return xc.atmos.growing_season_length(
            thresh=thresh,
            **params,
        )


class HD17:
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
        thresh = thresh_string(thresh, "mm/day")
        return xc.atmos.wet_precip_accumulation(
            thresh=thresh,
            **params,
        )


class RR:
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


class RR1:
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


class RDYYp:

    perc = 75
    base_period_time_range = BASE_PERIOD

    def compute(
        perc=perc,
        base_period_time_range=base_period_time_range,
        **params,
    ):
        """Calculate number of wet days with daily precip over a given percentile.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#days_over_precip_doy_thresh

        Returns
        -------
        xarray.DataArray
            Number of wet days over a given percentile.
        """
        da = get_da(params, "pr")
        percentile = get_percentile(
            da=da,
            perc=perc,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.days_over_precip_doy_thresh(
            pr_per=percentile,
            **params,
        )


class RYYmm:

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
        thresh = thresh_string(thresh, "mm/day")
        return xc.atmos.wetdays(
            thresh=thresh,
            **params,
        )


class RX1day:
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


class RYYpTOT:

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
        da = get_da(params, "pr")
        percentile = get_percentile(
            da=da,
            perc=perc,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.fraction_over_precip_thresh(
            pr_per=percentile,
            **params,
        )


class SDII:
    def compute(**params):
        """Calculate average precipitation during wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.daily_pr_intensity

        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Average precipitation during wet days.
        """
        return xc.atmos.daily_pr_intensity(**params)


class SU:

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
        thresh = thresh_string(thresh, "degC")
        return xc.atmos.tx_days_above(
            thresh=thresh,
            **params,
        )


class SQI:
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
        thresh = thresh_string(thresh, "degC")
        return xc.atmos.tn_days_above(
            thresh=thresh,
            **params,
        )


class TG:
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

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate fraction of days with mean temperature < 10th percentile".

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tg10p

        Returns
        -------
        xarray.DataArray
            Fraction of days with mean temperature < 10th percentile".
        """
        da = get_da(params, "tas")
        percentile = get_percentile(
            da=da,
            perc=10,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.tg10p(
            tas_per=percentile,
            **params,
        )


class TG90p:
    base_period_time_range = (BASE_PERIOD,)

    def compute(base_period_time_range=base_period_time_range, **params):
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
        da = get_da(params, "tas")
        percentile = get_percentile(
            da=da,
            perc=90,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.tg90p(
            tas_per=percentile,
            **params,
        )


class TR:
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
        thresh = thresh_string(thresh, "degC")
        return xc.atmos.tn_days_above(
            thresh=thresh,
            **params,
        )


class TX:
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

    base_period_time_range = (BASE_PERIOD,)

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate fraction of days with maximum temperature < 10th percentile".

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tx10p

        Returns
        -------
        xarray.DataArray
            Fraction of days with maximum temperature < 10th percentile".
        """
        da = get_da(params, "tasmax")
        percentile = get_percentile(
            da=da,
            perc=10,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.tx10p(
            tasmax_per=percentile,
            **params,
        )


class TX90p:

    base_period_time_range = (BASE_PERIOD,)

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate fraction of days with maximum temperature > 90th percentile".

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tx90p

        Returns
        -------
        xarray.DataArray
            Fraction of days with maximum temperature > 90th percentile".
        """
        da = get_da(params, "tasmax")
        percentile = get_percentile(
            da=da,
            perc=90,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.tx90p(
            tasmax_per=percentile,
            **params,
        )


class TXn:
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

    base_period_time_range = (BASE_PERIOD,)

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate fraction of days with minimum temperature < 10th percentile".

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tn10p

        Returns
        -------
        xarray.DataArray
            Fraction of days with minimum temperature < 10th percentile".
        """
        da = get_da(params, "tasmin")
        percentile = get_percentile(
            da=da,
            perc=10,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.tn10p(
            tasmin_per=percentile,
            **params,
        )


class TN90p:

    base_period_time_range = (BASE_PERIOD,)

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate fraction of days with minimum temperature > 90th percentile".

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#xclim.indicators.atmos.tx90p

        Returns
        -------
        xarray.DataArray
            Fraction of days with minimum temperature > 90th percentile".
        """
        da = get_da(params, "tasmin")
        percentile = get_percentile(
            da=da,
            perc=90,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.tn90p(
            tasmin_per=percentile,
            **params,
        )


class TNn:
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

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate number of warm and dry days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#warm_and_dry_days

        Returns
        -------
        Number of days where warm and dry conditions coincide.
        """
        da_tas = get_da(params, "tas")
        da_pr = get_da(params, "pr")
        percentile_tas = get_percentile(
            da=da_tas,
            perc=75,
            base_period_time_range=base_period_time_range,
        )
        percentile_pr = get_percentile(
            da=da_pr,
            perc=25,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.warm_and_dry_days(
            tas_per=percentile_tas,
            pr_per=percentile_pr,
            **params,
        )


class WSDI:

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
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
        da = get_da(params, "tasmax")
        percentile = get_percentile(
            da=da,
            perc=90,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.warm_spell_duration_index(
            tasmax_per=percentile,
            window=6,
            **params,
        )


class WW:

    base_period_time_range = BASE_PERIOD

    def compute(base_period_time_range=base_period_time_range, **params):
        """Calculate number of warm and wet days.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#warm_and_wet_days

        Returns
        -------
        Number of days where warm and wet conditions coincide.
        """
        da_tas = get_da(params, "tas")
        da_pr = get_da(params, "pr")
        percentile_tas = get_percentile(
            da=da_tas,
            perc=75,
            base_period_time_range=base_period_time_range,
        )
        percentile_pr = get_percentile(
            da=da_pr,
            perc=75,
            base_period_time_range=base_period_time_range,
        )
        return xc.atmos.warm_and_wet_days(
            tas_per=percentile_tas,
            pr_per=percentile_pr,
            **params,
        )
