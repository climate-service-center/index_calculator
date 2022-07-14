import xclim as xc


def thresh_string(thresh, units):
    if isinstance(thresh, str):
        return thresh
    else:
        return "{} {}".format(str(thresh), units)


class CDD:
    parameters = {
        "thresh": 0.1,
    }

    def compute(thresh=parameters["thresh"], **params):
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


class CSU:
    parameters = {
        "thresh": 25,
    }

    def compute(thresh=parameters["thresh"], **params):
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


class CWD:
    parameters = {
        "thresh": 0.1,
    }

    def compute(thresh=parameters["thresh"], **params):
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
    parameters = {
        "thresh": 0.1,
    }

    def compute(thresh=parameters["thresh"], **params):
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


class FD:
    parameters = {}

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
    parameters = {}

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


class RR:
    parameters = {}

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
    parameters = {}

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
    parameters = {}

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
    parameters = {}

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
    parameters = {}

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


class RX1day:
    parameters = {}

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


class RX5day:
    parameters = {}

    def compute(**params):
        """Calculate maximum 5-day total precipitation.

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#max_n_day_precipitation_amount

        Returns
        -------
        xarray.DataArray
            Maximum 5-day total precipitation.
        """
        return xc.atmos.max_n_day_precipitation_amount(
            window=5,
            **params,
        )


class SDII:
    parameters = {}

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
    parameters = {
        "thresh": 25,
    }

    def compute(thresh=parameters["thresh"], **params):
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
    parameters = {
        "thresh": 18,
    }

    def compute(thresh=parameters["thresh"], **params):
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
    parameters = {}

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


class TR:
    parameters = {
        "thresh": 20,
    }

    def compute(thresh=parameters["thresh"], **params):
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
    parameters = {}

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


class TXn:
    parameters = {}

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
    parameters = {}

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
    parameters = {}

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


class TNn:
    parameters = {}

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
    parameters = {}

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
