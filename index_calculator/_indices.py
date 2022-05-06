import xclim as xc

from ._consts import _freq


class ClimateIndices:
    def TG(self, ds, freq):
        return xc.atmos.tg_mean(ds=ds, freq=_freq[freq])
