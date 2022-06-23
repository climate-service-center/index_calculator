import xclim as xc

from ._consts import _freq


class ClimateIndices:
    """Class for calling xclim to calcualte cliamte indices."""

    def TG(self, ds, freq):
        """Calculate mean daily mean temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tas`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Mean daily mean temperature.
        """
        return xc.atmos.tg_mean(ds=ds, freq=_freq[freq])

    def RR(self, ds, freq):
        """Calculate total precipitation.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Total precipitation.
        """
        return xc.atmos.precip_accumulation(ds=ds, freq=_freq[freq])

    def SDII(self, ds, freq):
        """Calculate average precipitation during wet days.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Average precipitation during wet days.
        """
        return xc.atmos.daily_pr_intensity(ds=ds, freq=_freq[freq])

    def RR1(self, ds, freq):
        """Calculate number of wet days (pr >= 1 mm/day).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 1 mm/day).
        """
        return xc.atmos.wetdays(ds=ds, thresh="1 mm/day", freq=_freq[freq])

    def R10mm(self, ds, freq):
        """Calculate number of wet days (pr >= 10 mm/day).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 10 mm/day).
        """
        return xc.atmos.wetdays(ds=ds, thresh="10 mm/day", freq=_freq[freq])

    def R20mm(self, ds, freq):
        """Calculate number of wet days (pr >= 20 mm/day).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 20 mm/day).
        """
        return xc.atmos.wetdays(ds=ds, thresh="20 mm/day", freq=_freq[freq])

    def R25mm(self, ds, freq):
        """Calculate number of wet days (pr >= 25 mm/day).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of wet days (pr >= 25 mm/day).
        """
        return xc.atmos.wetdays(ds=ds, thresh="25 mm/day", freq=_freq[freq])

    def CDD(self, ds, freq):
        """Calculate maximum consecutive dry days (pr < 1 mm/day).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum consecutive dry days (pr < 1 mm/day).
        """
        return xc.atmos.maximum_consecutive_dry_days(ds=ds, freq=_freq[freq])

    def CWD(self, ds, freq):
        """Calculate maximum consecutive wet days (pr >= 1 mm/day).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum consecutive wet days (pr >= 1 mm/day).
        """
        return xc.atmos.maximum_consecutive_wet_days(ds=ds, freq=_freq[freq])

    def RX1day(self, ds, freq):
        """Calculate maximum 1-day total precipitation.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum 1-day total precipitation.
        """
        return xc.atmos.max_1day_precipitation_amount(ds=ds, freq=_freq[freq])

    def RX5day(self, ds, freq):
        """Calculate maximum 5-day total precipitation.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `pr`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum 5-day total precipitation.
        """
        return xc.atmos.max_n_day_precipitation_amount(
            ds=ds, window=5, freq=_freq[freq]
        )

    def TR(self, ds, freq):
        """Calculate number of tropical nights (tasmin > 20.0 degC).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmin`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of tropical nights (tasmin > 20.0 degC).
        """
        return xc.atmos.tropical_nights(ds=ds, freq=_freq[freq], thres=20)

    def FD(self, ds, freq):
        """Calculate number of frost days (tasmin < 0.0 degC).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmin`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of frost days (tasmin < 0.0 degC).
        """
        return xc.atmos.frost_days(ds=ds, freq=_freq[freq])

    def ID(self, ds, freq):
        """Calculate number of ice days (tasmax < 0.0 degC).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmax`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of ice days (tasmax < 0.0 degC).
        """
        return xc.atmos.ice_days(ds=ds, freq=_freq[freq])

    def TX(self, ds, freq):
        """Calculate mean daily maximum temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmax`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Mean daily maximum temperature.
        """
        return xc.atmos.tx_mean(ds=ds, freq=_freq[freq])

    def TXn(self, ds, freq):
        """Calculate minimum daily maximum temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmax`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Minimum daily maximum temperature.
        """
        return xc.atmos.tx_min(ds=ds, freq=_freq[freq])

    def TXx(self, ds, freq):
        """Calculate maximum daily maximum temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmax`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum daily maximum temperature.
        """
        return xc.atmos.tx_max(ds=ds, freq=_freq[freq])

    def TN(self, ds, freq):
        """Calculate mean daily minimum temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmin`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Mean daily minimum temperature.
        """
        return xc.atmos.tn_mean(ds=ds, freq=_freq[freq])

    def TNn(self, ds, freq):
        """Calculate minimum daily minimum temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmin`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Minimum daily minimum temperature.
        """
        return xc.atmos.tn_min(ds=ds, freq=_freq[freq])

    def TNx(self, ds, freq):
        """Calculate maximum daily minimum temperature.

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmin`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum daily minimum temperature.
        """
        return xc.atmos.tn_max(ds=ds, freq=_freq[freq])

    def SU(self, ds, freq):
        """Calculate number of summer days (tasmax > 25.0 degC).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmax`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Number of summer days (tasmax > 25.0 degC).
        """
        return xc.atmos.tx_days_above(ds=ds, freq=_freq[freq], thresh=25)

    def CSU(self, ds, freq):
        """Calculate maximum consecutive summer days (tasmax > 25.0 degC).

        Parameters
        ----------
        ds: xarray.Dataset
            Database with varibale `tasmax`.
        freq: str
            Resampling frequency.

        Returns
        -------
        xarray.DataArray
            Maximum consecutive summer days (tasmax > 25.0 degC).
        """
        return xc.atmos.maximum_consecutive_warm_days(
            ds=ds,
            freq=_freq[freq],
            thresh=25,
        )
