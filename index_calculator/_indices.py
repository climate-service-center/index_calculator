import xclim as xc

from ._consts import _freq


class ClimateIndices:
    def TG(self, ds, freq):
        return xc.atmos.tg_mean(ds=ds, freq=_freq[freq])

    def RR(self, ds, freq):
        return xc.atmos.precip_accumulation(ds=ds, freq=_freq[freq])

    def SDII(self, ds, freq):
        return xc.atmos.daily_pr_intensity(ds=ds, freq=_freq[freq])

    def RR1(self, ds, freq):
        return xc.atmos.wetdays(ds=ds, thresh="1 mm/day", freq=_freq[freq])

    def R10mm(self, ds, freq):
        return xc.atmos.wetdays(ds=ds, thresh="10 mm/day", freq=_freq[freq])

    def R20mm(self, ds, freq):
        return xc.atmos.wetdays(ds=ds, thresh="20 mm/day", freq=_freq[freq])

    def R25mm(self, ds, freq):
        return xc.atmos.wetdays(ds=ds, thresh="25 mm/day", freq=_freq[freq])

    def CDD(self, ds, freq):
        return xc.atmos.maximum_consecutive_dry_days(ds=ds, freq=_freq[freq])

    def CWD(self, ds, freq):
        return xc.atmos.maximum_consecutive_wet_days(ds=ds, freq=_freq[freq])

    def RX1day(self, ds, freq):
        return xc.atmos.max_1day_precipitation_amount(ds=ds, freq=_freq[freq])

    def RX5day(self, ds, freq):
        return xc.atmos.max_n_day_precipitation_amount(
            ds=ds, window=5, freq=_freq[freq]
        )

    def TR(self, ds, freq):
        return xc.atmos.tropical_nights(ds=ds, freq=_freq[freq], thres=20)

    def FD(self, ds, freq):
        return xc.atmos.frost_days(ds=ds, freq=_freq[freq])

    def ID(self, ds, freq):
        return xc.atmos.ice_days(ds=ds, freq=_freq[freq])

    def TX(self, ds, freq):
        return xc.atmos.tx_mean(ds=ds, freq=_freq[freq])

    def TXn(self, ds, freq):
        return xc.atmos.tx_min(ds=ds, freq=_freq[freq])

    def TXx(self, ds, freq):
        return xc.atmos.tx_max(ds=ds, freq=_freq[freq])

    def TN(self, ds, freq):
        return xc.atmos.tn_mean(ds=ds, freq=_freq[freq])

    def TNn(self, ds, freq):
        return xc.atmos.tn_min(ds=ds, freq=_freq[freq])

    def TNx(self, ds, freq):
        return xc.atmos.tn_max(ds=ds, freq=_freq[freq])

    def SU(self, ds, freq):
        return xc.atmos.tx_days_above(ds=ds, freq=_freq[freq], thresh=25)

    def CSU(self, ds, freq):
        return xc.atmos.maximum_consecutive_tx_days(
            ds=ds,
            freq=_freq[freq],
            thresh=25,
        )
