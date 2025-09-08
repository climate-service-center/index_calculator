import xclim as xc

from ._climate_indicator import ClimateIndicator


class CD(ClimateIndicator):
    """Number of cold and dry days (tas, pr)."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tas_per": {
                "variable": "tas",
                "per": 25,
                "method": "temperature",
            },
            "pr_per": {
                "variable": "pr",
                "per": 25,
                "method": "precipitation",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tas_per=tas_per,
            pr_per=pr_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class CDD(ClimateIndicator):
    """Maximum consecutive dry days (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class CFD(ClimateIndicator):
    """Maximum number of consecutive frost days (tasmin)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class CHDYYx(ClimateIndicator):
    """Maximum number of consecutive heat days (tasmax)."""

    def __init__(self):
        super().__init__()
        self.thresh = 30
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class CSDI(ClimateIndicator):
    """Cold spell duration index (tasmin)."""

    def __init__(self):
        super().__init__()
        self.window = 6
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
        percentiles = {
            "tasmin_per": {
                "variable": "tasmin",
                "per": 10,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            window=window,
            tasmin_per=tasmin_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class CSU(ClimateIndicator):
    """Maximum consecutive summer days (tasmax)."""

    def __init__(self):
        super().__init__()
        self.thresh = 25
        self.units = {"thresh": "degC"}
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
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.maximum_consecutive_warm_days
        """
        return self.compute_climate_indicator(params=params, thresh=thresh)


class CW(ClimateIndicator):
    """Number of cold and wet days (tas, pr)."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tas_per": {
                "variable": "tas",
                "per": 25,
                "method": "temperature",
            },
            "pr_per": {
                "variable": "pr",
                "per": 75,
                "method": "precipitation",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tas_per=tas_per,
            pr_per=pr_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class CWD(ClimateIndicator):
    """Consecutive wet days (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class DD(ClimateIndicator):
    """Number of dry days (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class DSf(ClimateIndicator):
    """Number of dry spells (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.window = 5
        self.units = {"thresh": "mm"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class DSx(ClimateIndicator):
    """Maximum length of dry spells (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.window = 1
        self.units = {"thresh": "mm"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class DSn(ClimateIndicator):
    """Total number of days in dry spells (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.window = 5
        self.units = {"thresh": "mm"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class WSf(ClimateIndicator):
    """Number of wet spells (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.window = 5
        self.units = {"thresh": "mm"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class WSx(ClimateIndicator):
    """Maximum length of wet spells (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.window = 1
        self.units = {"thresh": "mm"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class WSn(ClimateIndicator):
    """Total number of days in wet spells (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.window = 5
        self.units = {"thresh": "mm"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class DTR(ClimateIndicator):
    """Mean temperature rnage (tasmax, tasmin)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class FD(ClimateIndicator):
    """Number of frost days (tasmin)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class LFD(ClimateIndicator):
    """Number of late frost days (tasmin)."""

    def __init__(self):
        super().__init__()
        self.start_date = "04-01"
        self.end_date = "06-30"
        self.date_bounds = True
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
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.late_frost_days
        """
        return self.compute_climate_indicator(
            params=params, start_date=start_date, end_date=end_date
        )


class ID(ClimateIndicator):
    """Number of ice days (tasmax)."""

    def __init__(self):
        super().__init__()
        self.func = xc.atmos.ice_days

    def compute(self, **params):
        """Calculate number of ice days (tasmax < 0.0 degC).

        Returns
        -------
        xarray.DataArray
            Number of ice days (tasmax < 0.0 degC).

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.ice_days
        """
        return self.compute_climate_indicator(params=params)


class GD(ClimateIndicator):
    """Cumulative growing degree days (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = 4
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class HD17(ClimateIndicator):
    """Cumulative heating degree days (tas)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class PRCPTOT(ClimateIndicator):
    """Total precipitation amount (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class RR(ClimateIndicator):
    """Total precipitation (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class RRm(ClimateIndicator):
    """Mean daily precipitation (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class RR1(ClimateIndicator):
    """Number of wet days (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params, thresh="1 mm/day")


class R10mm(ClimateIndicator):
    """Number of heavy precipitation days (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(
            params=params,
            thresh="10 mm/day",
        )


class R20mm(ClimateIndicator):
    """Number of very heavy precipitation days (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(
            params=params,
            thresh="20 mm/day",
        )


class R25mm(ClimateIndicator):
    """Number of super heavy precipitation days (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(
            params=params,
            thresh="25 mm/day",
        )


class RRYYp(ClimateIndicator):
    """Precip percentil value for wet days (pr)."""

    def __init__(self):
        super().__init__()
        self.per = 75
        self.thresh = 1
        self.units = {"thresh": "mm/day"}

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
        percentiles = {
            "pr_per": {
                "variable": "pr",
                "per": per,
                "method": "precipitation",
                "thresh": thresh,
            },
        }
        results = self.compute_climate_indicator(
            params=params,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )
        return results["pr_per"]


class RYYp(ClimateIndicator):
    """Number of wet days with precip over a given percentile (pr)."""

    def __init__(self):
        super().__init__()
        self.per = 75
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        percentiles = {
            "pr_per": {
                "variable": "pr",
                "per": per,
                "method": "precipitation",
                "thresh": thresh,
            },
        }
        return self.compute_climate_indicator(
            params=params,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class RYYmm(ClimateIndicator):
    """Number of days with precip over threshold (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 25
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class RX1day(ClimateIndicator):
    """Maximum 1-day total precipitation (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class RXYYday(ClimateIndicator):
    """Maximum n-day total precipitation (pr)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params, window=window)


class RYYpTOT(ClimateIndicator):
    """Precipitation fraction with precip above percentile on wet days (pr)"""

    def __init__(self):
        super().__init__()
        self.per = 75
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        percentiles = {
            "pr_per": {
                "variable": "pr",
                "per": per,
                "method": "precipitation",
                "thresh": thresh,
            },
        }
        return self.compute_climate_indicator(
            params=params,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class SDII(ClimateIndicator):
    """Average precipitation during wet days (pr)."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class SU(ClimateIndicator):
    """Number of summer days (tasmax)."""

    def __init__(self):
        super().__init__()
        self.thresh = 25
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class CMD(ClimateIndicator):
    """Number of calm days (sfcWind)."""

    def __init__(self):
        super().__init__()
        self.thresh = 2
        self.units = {"thresh": "m s-1"}
        self.func = xc.atmos.calm_days

    def compute(self, thresh=None, **params):
        """Calculate number of calm days.

        Parameters
        ----------
        thresh: int or string, optional
            Threshold wind speed below which a day is considered
            as a calm day (default: 2 m s-1).
            If type of threshold is an integer the unit is set to m s-1.

        Returns
        -------
        xarray.DataArray
            Number of calm days ( fg > {thresh}).

        Notes
        -----
        For more information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.calm_days

        """
        return self.compute_climate_indicator(params=params, thresh=thresh)


class SQI(ClimateIndicator):
    """Number of uncomfortable sleep events (tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh = 18
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class TG(ClimateIndicator):
    """Mean mean temperature (tas)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class TG10p(ClimateIndicator):
    """Fraction of days with mean temperature < 10th percentile (tas)."""

    def __init__(self):
        super().__init__()
        self.tas_per = None
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
        percentiles = {
            "tas_per": {
                "variable": "tas",
                "per": 10,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tas_per=tas_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class TG90p(ClimateIndicator):
    """Fraction of days with mean temperature > 90th percentile (tas)."""

    def __init__(self):
        super().__init__()
        self.func = xc.atmos.tg90p

    def compute(
        self,
        base_period_time_range=None,
        tas_per=None,
        **params,
    ):
        """Calculate fraction of days with mean temperature > 90th percentile.

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
        percentiles = {
            "tas_per": {
                "variable": "tas",
                "per": 90,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tas_per=tas_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class TR(ClimateIndicator):
    """Number of tropical nights (tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh = 20
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class TX(ClimateIndicator):
    """Mean maximum temperature (tasmax)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class TX10p(ClimateIndicator):
    """Fraction of days with max temperature < 10th percentile (tasmax)."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tasmax_per": {
                "variable": "tasmax",
                "per": 10,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tasmax_per=tasmax_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class TX90p(ClimateIndicator):
    """Fraction of days with max temperature > 90th percentile (tasmax)."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tasmax_per": {
                "variable": "tasmax",
                "per": 90,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tasmax_per=tasmax_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class TXn(ClimateIndicator):
    """Minimum maximum temperature (tasmax)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class TXx(ClimateIndicator):
    """Maximum maximum temperature (tasmax)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class TN(ClimateIndicator):
    """Mean minimum temperature (tasmin)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class TN10p(ClimateIndicator):
    """Fraction of days with min temperature < 10th percentile."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tasmin_per": {
                "variable": "tasmin",
                "per": 10,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tasmin_per=tasmin_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class TN90p(ClimateIndicator):
    """Fraction of days with min temperature > 90th percentile."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tasmin_per": {
                "variable": "tasmin",
                "per": 90,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tasmin_per=tasmin_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class TNn(ClimateIndicator):
    """Minimum minimum temperature (tasmin)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class TNx(ClimateIndicator):
    """Maximum minimum temperature (tasmin)."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class WD(ClimateIndicator):
    """Number of warm and dry days (tas, pr)."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tas_per": {
                "variable": "tas",
                "per": 75,
                "method": "temperature",
            },
            "pr_per": {
                "variable": "pr",
                "per": 25,
                "method": "precipitation",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tas_per=tas_per,
            pr_per=pr_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class WSDI(ClimateIndicator):
    """Warm spell duration index (tasmax)."""

    def __init__(self):
        super().__init__()
        self.window = 6
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
        percentiles = {
            "tasmax_per": {
                "variable": "tasmax",
                "per": 90,
                "method": "temperature",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            window=window,
            tasmax_per=tasmax_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class WW(ClimateIndicator):
    """Number of warm and wet days (tas, pr)."""

    def __init__(self):
        super().__init__()
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
        percentiles = {
            "tas_per": {
                "variable": "tas",
                "per": 75,
                "method": "temperature",
            },
            "pr_per": {
                "variable": "pr",
                "per": 75,
                "method": "precipitation",
            },
        }
        return self.compute_climate_indicator(
            params=params,
            tas_per=tas_per,
            pr_per=pr_per,
            percentiles=percentiles,
            base_period_time_range=base_period_time_range,
        )


class CSf(ClimateIndicator):
    """Number of cold spells (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = -10
        self.window = 3
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class CSx(ClimateIndicator):
    """Maximum length of cold spells (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = -10
        self.window = 1
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class CSn(ClimateIndicator):
    """Total number of days in cold spells (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = -10
        self.window = 3
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class HSf(ClimateIndicator):
    """Number of hot spells (tasmax)."""

    def __init__(self):
        super().__init__()
        self.thresh = 35
        self.window = 3
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class HSx(ClimateIndicator):
    """Maximum lenght of hot spells (tasmax)."""

    def __init__(self):
        super().__init__()
        self.thresh = 35
        self.window = 1
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class HSn(ClimateIndicator):
    """Total number of days in hot spells (tasmax)."""

    def __init__(self):
        super().__init__()
        self.thresh = 35
        self.window = 3
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class SD(ClimateIndicator):
    """Number of snow days."""

    def __init__(self):
        super().__init__()
        self.low = 1
        self.units = {"low": "mm/day"}
        self.func = xc.atmos.days_with_snow

    def compute(self, low=None, **params):
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
        return self.compute_climate_indicator(params=params, low=low)


class SCD(ClimateIndicator):
    """Snow cover duration."""

    def __init__(self):
        super().__init__()
        self.thresh = 3
        self.units = {"thresh": "cm"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class Sint(ClimateIndicator):
    """Snowfall intensity."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class Sfreq(ClimateIndicator):
    """Snowfall frequency."""

    def __init__(self):
        super().__init__()
        self.thresh = 1
        self.units = {"thresh": "mm/day"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class UTCI(ClimateIndicator):
    """Universal thermal climate index."""

    def __init__(self):
        super().__init__()
        self.stat = "sunlit"
        self.mask_invalid = True
        self.func = xc.indicators.convert.universal_thermal_climate_index

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
        return self.compute_climate_indicator(
            params=params, stat=stat, mask_invalid=mask_invalid
        )


class WI(ClimateIndicator):
    """Number of winter days (tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh = -10
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(params=params, thresh=thresh)


class HWf(ClimateIndicator):
    """Number of heat waves (tasmax, tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh_tasmin = 22
        self.thresh_tasmax = 30
        self.window = 3
        self.units = {"thresh_tasmin": "degC", "thresh_tasmax": "degC"}
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
        return self.compute_climate_indicator(
            params=params,
            thresh_tasmin=thresh_tasmin,
            thresh_tasmax=thresh_tasmax,
            window=window,
        )


class HWx(ClimateIndicator):
    """Maximum length of heat waves (tasmax, tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh_tasmin = 22
        self.thresh_tasmax = 30
        self.window = 1
        self.units = {"thresh_tasmin": "degC", "thresh_tasmax": "degC"}
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
        return self.compute_climate_indicator(
            params=params,
            thresh_tasmin=thresh_tasmin,
            thresh_tasmax=thresh_tasmax,
            window=window,
        )


class HWn(ClimateIndicator):
    """Total number of days in heat waves (tasmax, tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh_tasmin = 22
        self.thresh_tasmax = 30
        self.window = 3
        self.units = {"thresh_tasmin": "degC", "thresh_tasmax": "degC"}
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
        return self.compute_climate_indicator(
            params=params,
            thresh_tasmin=thresh_tasmin,
            thresh_tasmax=thresh_tasmax,
            window=window,
        )


class GSS(ClimateIndicator):
    """Growing season start (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = 5
        self.window = 5
        self.units = {"thresh": "degC"}
        self.func = xc.atmos.growing_season_start

    def compute(self, thresh=None, window=None, mid_date=None, **params):
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
        return self.compute_climate_indicator(
            params=params,
            thresh=thresh,
            window=window,
            mid_date=mid_date,
        )


class GSE(ClimateIndicator):
    """Growing season end (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = 5
        self.window = 5
        self.units = {"thresh": "degC"}
        self.func = xc.atmos.growing_season_end

    def compute(self, thresh=None, window=None, mid_date=None, **params):
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
        return self.compute_climate_indicator(
            params=params,
            thresh=thresh,
            window=window,
            mid_date=mid_date,
        )


class GSL(ClimateIndicator):
    """Growing season length (tas)."""

    def __init__(self):
        super().__init__()
        self.thresh = 5
        self.window = 5
        self.mid_date = "07-01"
        self.freq = "YS"
        self.units = {"thresh": "degC"}
        self.func = xc.atmos.growing_season_length

    def compute(self, thresh=None, window=None, mid_date=None, **params):
        """Calculate growing season length.

        Parameters
         ----------
         thresh: Threshold temperature on which to base evaluation.
             (default: 5 degC). If type of threshold is an integer
             the unit is set to degC.
         window: int, optional
             Minimum number of days with temperature above threshold
             to mark the beginning and end of growing season (default: 5).
         mid_date: (date (string, MM-DD)) – Date of the year
             after which to look for the end of the season.
             Should have the format ‘%m-%d’. Default : 07-01

         Returns
         -------
         xarray.DataArray
             Growing season length.

         Notes
         -----
         For more information on the input parameters see:
             https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.growing_season_length
        """
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class FFS(ClimateIndicator):
    """Frost free season start (tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh = 0
        self.window = 5
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class FFE(ClimateIndicator):
    """Frost free season end (tasmin)."""

    def __init__(self):
        super().__init__()
        self.thresh = 0
        self.window = 5
        self.units = {"thresh": "degC"}
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
        return self.compute_climate_indicator(
            params=params, thresh=thresh, window=window
        )


class FG(ClimateIndicator):
    """Mean daily mean wind speed."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class FGn(ClimateIndicator):
    """Minimum daily mean wind speed."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class FGx(ClimateIndicator):
    """Maximum daily mean wind speed."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class FX(ClimateIndicator):
    """Mean daily maximum wind speed."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class FXn(ClimateIndicator):
    """Minimum daily maximum wind speed."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class FXx(ClimateIndicator):
    """Maximum daily maximum wind speed."""

    def __init__(self):
        super().__init__()
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
        return self.compute_climate_indicator(params=params)


class HIX(ClimateIndicator):
    """temperature felt by a person.

    When relative humidity is taken into account (tas, hurs)

    """

    def __init__(self):
        super().__init__()
        self.func = xc.indicators.convert.humidex

    def compute(self, **params):
        """Calculate maximum number of consecutive heat days.

        Returns
        -------
        xarray.DataArray
            temperature felt by a person when relative humidity
            is taken into account.

        Notes
        -----
        For information on the input parameters see:
            https://xclim.readthedocs.io/en/stable/api.html#xclim.indicators.atmos.humidex
        """
        return self.compute_climate_indicator(params=params)
