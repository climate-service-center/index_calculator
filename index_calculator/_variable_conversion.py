import inspect

import xclim as xc


class ConvertVariables:
    def __init__(self, ds, **params):
        self.ds = ds
        self.params = params

    def _params(self, func, params):
        fparams = inspect.signature(func).parameters
        return {k: v for k, v in params.items() if k in fparams.keys()}

    def sfcWind(self):
        return xc.atmos.wind_speed_from_vector(
            ds=self.ds,
        )[0]

    def snd(self):
        params = self._params(xc.land.snw_to_snd, self.params)
        return xc.land.snw_to_snd(ds=self.ds, **params)
