import os
import warnings
from pathlib import Path

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

    def parse_components_to_format(self, out_components, out_format):
        def test_ocomp(ocomp):
            return ocomp.replace("/", "")

        ocomps = []
        for comp in out_components:
            if hasattr(self.proc, comp):
                ocomps.append(test_ocomp(getattr(self.proc, comp)))
            elif hasattr(self.ds, comp):
                ocomps.append(test_ocomp(getattr(self.ds, comp)))
            else:
                ocomps.append("NA")
                warnings.warn(f"{comp} not found!")
        return out_format.format(*ocomps)

    def outname(self):
        """Set project-specific ouput file name."""

        try:
            output_fmt = pjson[self.project]["format"]
            output_comps = pjson[self.project]["components"].split(", ")
        except ValueError:
            warnings.warn(f"Project {self.project} not known")
            return

        return self.parse_components_to_format(output_comps, output_fmt)

    def directory_structure(self):
        """Set project-specific directory structure."""
        try:
            output_fmt = pjson[self.project]["drs_format"]
            output_comps = pjson[self.project]["drs_components"].split(", ")
        except ValueError:
            warnings.warn(f"Project {self.project} not known")
            return
        return self.parse_components_to_format(output_comps, output_fmt)

    def to_netcdf(self):
        """Write xarray.Dataset to netCDF file on disk."""
        ds = save_xrdataset(
            self.postproc,
            name=self.outputname,
            encoding_dict={"encoding": self.encoding},
        )
        print(f"File written: {self.outputname}")
        return ds

    def write_to_netcdf(
        self,
        output_name=True,
        output_dir=".",
        drs=True,
        project=None,
        **kwargs,
    ):
        """Write xarray.Dataset to disk.

        Set default project-specific ouput name.
        """
        write = False

        if output_name is True:
            if self.project is None:
                self.project = project
            if self.project is None:
                raise ValueError("No project is selected. 'project=...'.")
            outputname = self.outname()
            if outputname:
                write = True
            else:
                warnings.warn("Could not write output.")
        elif isinstance(output_name, str):
            outputname = output_name
            write = True
        if drs is True:
            output_dir = os.path.join(output_dir, self.directory_structure())
        os.makedirs(output_dir, exist_ok=True)
        self.outputname = Path(os.path.join(output_dir, outputname)).resolve()
        if write:
            return self.to_netcdf()
