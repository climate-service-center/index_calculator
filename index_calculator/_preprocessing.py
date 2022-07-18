import pyhomogenize as pyh

from ._consts import _bounds, _fmt
from ._utils import get_time_range_as_str, kwargs_to_self


class PreProcessing:
    """Class for pre-processing."""

    def __init__(
        self,
        ds=None,
        var_name=None,
        freq="year",
        time_range=None,
        crop_time_axis=True,
        check_time_axis=True,
        **kwargs,
    ):
        """Write parameters to self."""
        if ds is None:
            raise ValueError("Please select an input xarray dataset. 'ds=...'")
        self.ds = ds
        self.var_name = var_name
        self.freq = freq
        self.fmt = _fmt[freq]
        self.afmt = _fmt[ds.frequency]
        self.time_range = time_range
        self.crop_time_axis = crop_time_axis
        self.check_time_axis = check_time_axis
        kwargs_to_self(kwargs, self)
        self.preproc = self.preprocessing()

    def preprocessing(self):
        """Select and check time range."""

        time_control = pyh.time_control(self.ds)
        if not self.var_name:
            self.var_name = time_control.name

        avail_time = get_time_range_as_str(time_control.time, self.afmt)

        if self.time_range:
            time_control.select_time_range(self.time_range)
        if self.crop_time_axis:
            time_control.select_limited_time_range(
                smonth=_bounds[self.freq]["start"],
                emonth=_bounds[self.freq]["end"],
            )
        req_time = get_time_range_as_str(time_control.time, self.fmt)

        if self.check_time_axis:
            time_control.check_timestamps(correct=True)

        self.TimeRange = req_time
        self.ATimeRange = avail_time

        return time_control.ds
