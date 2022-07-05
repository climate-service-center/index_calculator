import xclim as xc


class ClimateIndices:
    """Class for calling xclim to calculate climate indices."""

    def TG(self, *args, **kwargs):
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
        return xc.atmos.tg_mean(
            *args,
            **kwargs,
        )

    def RR(self, *args, **kwargs):
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
        return xc.atmos.precip_accumulation(
            *args,
            **kwargs,
        )

    def SDII(self, *args, **kwargs):
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
        return xc.atmos.daily_pr_intensity(
            *args,
            **kwargs,
        )

    def RR1(self, *args, **kwargs):
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
            *args,
            **kwargs,
        )

    def R10mm(self, *args, **kwargs):
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
            *args,
            **kwargs,
        )

    def R20mm(self, *args, **kwargs):
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
            *args,
            **kwargs,
        )

    def R25mm(self, *args, **kwargs):
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
            *args,
            **kwargs,
        )

    def CDD(self, *args, **kwargs):
        """Calculate maximum consecutive dry days (pr < 1 mm/day).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_dry_days

        Returns
        -------
        xarray.DataArray
            Maximum consecutive dry days (pr < 1 mm/day).
        """
        return xc.atmos.maximum_consecutive_dry_days(
            *args,
            **kwargs,
        )

    def CWD(self, *args, **kwargs):
        """Calculate maximum consecutive wet days (pr >= 1 mm/day).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_wet_days

        Returns
        -------
        xarray.DataArray
            Maximum consecutive wet days (pr >= 1 mm/day).
        """
        return xc.atmos.maximum_consecutive_wet_days(
            *args,
            **kwargs,
        )

    def RX1day(self, *args, **kwargs):
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
        return xc.atmos.max_1day_precipitation_amount(
            *args,
            **kwargs,
        )

    def RX5day(self, *args, **kwargs):
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
            *args,
            **kwargs,
        )

    def TR(self, *args, **kwargs):
        """Calculate number of tropical nights (tasmin > 20.0 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tropical_nights

        Returns
        -------
        xarray.DataArray
            Number of tropical nights (tasmin > 20.0 degC).
        """
        return xc.atmos.tropical_nights(
            thres=20,
            *args,
            **kwargs,
        )

    def FD(self, *args, **kwargs):
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
        return xc.atmos.frost_days(
            *args,
            **kwargs,
        )

    def ID(self, *args, **kwargs):
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
        return xc.atmos.ice_days(
            *args,
            **kwargs,
        )

    def TX(self, *args, **kwargs):
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
        return xc.atmos.tx_mean(
            *args,
            **kwargs,
        )

    def TXn(self, *args, **kwargs):
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
        return xc.atmos.tx_min(
            *args,
            **kwargs,
        )

    def TXx(self, *args, **kwargs):
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
        return xc.atmos.tx_max(
            *args,
            **kwargs,
        )

    def TN(self, *args, **kwargs):
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
        return xc.atmos.tn_mean(
            *args,
            **kwargs,
        )

    def TNn(self, *args, **kwargs):
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
        return xc.atmos.tn_min(
            *args,
            **kwargs,
        )

    def TNx(self, *args, **kwargs):
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
        return xc.atmos.tn_max(
            *args,
            **kwargs,
        )

    def SU(self, *args, **kwargs):
        """Calculate number of summer days (tasmax > 25.0 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#tx_days_above

        Returns
        -------
        xarray.DataArray
            Number of summer days (tasmax > 25.0 degC).
        """
        return xc.atmos.tx_days_above(
            thresh=25,
            *args,
            **kwargs,
        )

    def CSU(self, *args, **kwargs):
        """Calculate maximum consecutive summer days (tasmax > 25.0 degC).

        Parameters
        ----------
        For input parameters see:
            https://xclim.readthedocs.io/en/stable/indicators_api.html#maximum_consecutive_warm_days

        Returns
        -------
        xarray.DataArray
            Maximum consecutive summer days (tasmax > 25.0 degC).
        """
        return xc.atmos.maximum_consecutive_warm_days(
            thresh=25,
            *args,
            **kwargs,
        )
