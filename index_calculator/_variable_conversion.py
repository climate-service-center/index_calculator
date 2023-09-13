import xclim as xc


class ConvertVariables:
    def __init__(self, ds, **params):
        self.ds = ds
        self.params = params

    def sfcWind(self):
        return xc.atmos.wind_speed_from_vector(
            ds=self.ds,
        )[0]

    def snd(self):
        return xc.land.snw_to_snd(ds=self.ds, **self.params)
