import warnings

from ._tables import pjson
from ._utils import object_attrs_to_self


class OutputWriter:
    """Class for writing xarray.Dataset to disk.

    Set default project-specific ouput name.
    """

    def __init__(
        self,
        outname=None,
        postproc_obj=None,
        **kwargs,
    ):
        """Write parameters to self."""
        if postproc_obj is None:
            raise ValueError(
                "Please select an index_calculator.PostProcessing object."
                "'proc_obj=...'"
            )
        object_attrs_to_self(postproc_obj, self)

    def outname(self):
        """Set project-specific ouput file name."""

        def test_ocomp(ocomp):
            return ocomp.replace("/", "")

        drs = {}
        cproj = "climdex" + self.project
        try:
            drs["output_fmt"] = pjson[cproj]["format"]
            drs["output_comps"] = pjson[cproj]["components"].split(", ")
        except ValueError:
            warnings.warn(f"Project climdex{self.project} not known")
            return
        ocomps = []
        for comp in drs["output_comps"]:
            if hasattr(self.proc, comp):
                ocomps.append(test_ocomp(getattr(self.proc, comp)))
            elif hasattr(self.ds, comp):
                ocomps.append(test_ocomp(getattr(self.ds, comp)))
            else:
                ocomps.append("NA")
                warnings.warn(f"{comp} not found!")
        return drs["output_fmt"].format(*ocomps)

    def to_netcdf(self):
        """Write xarray.Dataset to netCDF file on disk."""
        MISSVAL = 1e20
        encoding = {
            self.CIname: {"_FillValue": MISSVAL, "missing_value": MISSVAL},
            "time": {
                "units": self.ds.time.encoding["units"],
                "calendar": self.ds.time.encoding["calendar"],
                "dtype": self.ds.time.encoding["dtype"],
            },
            "time_bnds": {
                "units": self.ds.time_bnds.encoding["units"],
                "calendar": self.ds.time_bnds.encoding["calendar"],
                "dtype": self.ds.time.encoding["dtype"],
            },
        }
        self.postproc.to_netcdf(
            self.outputname,
            encoding=encoding,
            format="NETCDF4",
            unlimited_dims={"time": True},
        )
        print(f"File written: {self.outputname}")

    def write_to_netcdf(self, output=True, project=None):
        """Write xarray.Dataset to disk.

        Set default project-specific ouput name.
        """
        write = False
        if output is True:
            if self.project is None:
                self.project = project
            if self.project is None:
                raise ValueError("No project is selected. 'project=...'.")
            self.outputname = self.outname()
            if self.outputname:
                write = True
            else:
                warnings.warn("Could not write output.")
        elif isinstance(output, str):
            self.outputname = output
            write = True
        if write:
            self.to_netcdf()
