import warnings

from pyhomogenize import save_xrdataset

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
        try:
            drs["output_fmt"] = pjson[self.project]["format"]
            drs["output_comps"] = pjson[self.project]["components"].split(", ")
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
        ds = save_xrdataset(
            self.postproc,
            name=self.outputname,
            encoding_dict={"encoding": self.encoding},
        )
        print(f"File written: {self.outputname}")
        return ds

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
            return self.to_netcdf()
