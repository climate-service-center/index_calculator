import os
import warnings
from pathlib import Path

from pyhomogenize import save_xrdataset

from ._tables import pjson
from ._utils import object_attrs_to_self


class OutputWriter:
    """Class for writing xarray.Dataset to disk.
    Get default project-specific output name.

    Parameters
    ----------
    postproc_obj: index_calculator.postprocessing or list
        ``index_calculator.postprocessing`` object
    output_name: bool or str (default: True), optional
        If True get project-specific output name.
        If `str` set output_name to that string.
    output_dir: str (default: "."), optional
        Set output directory
    drs: bool (default: True), optional
        If True create project-specific directory structure

    Example
    -------
    Write climate indicator dataset to disk::

        from pyhomogenize import open_xrdataset
        from index_calculator import preprocessing
        from index_calculator import processing
        from index_calculator import postprocessing
        from index_calculator import outputwriter

        netcdf_file = "tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_"
                      "GERICS-REMO2015_v1_day_20010101-20051231.nc"
        ds = open_xrdataset(netcdf_file)

        preproc = preprocessing(ds)
        proc = processing(index="TG", preproc_obj=preproc)
        postproc = postprocessing(
            project="CORDEX",
            proc_obj=proc,
            institution="Helmholtz-Zentrum hereon GmbH,"
                        "Climate Service Center Germany",
            institution_id="GERICS",
            contact="gerics-cordex@hereon.de",
        )
        outputwriter(postproc_obj=postproc)


        --> File written: cordex/climdex/EUR-11/GERICS/GERICS/MPI-M-MPI-ESM-LR/
                          historical/r3i1p1/GERICS-REMO2015/v1/year/TG/
                          TG_EUR-11_MPI-M-MPI-ESM-LR_historical_r3i1p1_
                          GERICS-REMO2015_v1_day_GERICS_year_2001-2005.nc

    """

    def __init__(
        self,
        postproc_obj=None,
        output_name=True,
        output_dir=".",
        drs=True,
        **kwargs,
    ):
        if postproc_obj is None:
            raise NameError(
                "Please select an index_calculator.PostProcessing object."
                "'proc_obj=...'"
            )
        object_attrs_to_self(postproc_obj, self)
        if isinstance(self.postproc, str):
            postprocs = [self.postproc]
        else:
            postprocs = self.postproc
        if drs is True:
            output_dir = os.path.join(
                output_dir, self._directory_structure(postprocs[0])
            )
        os.makedirs(output_dir, exist_ok=True)
        self.output_name = output_name
        ds_dict = {}
        for postproc in postprocs:
            ds_ = postproc.copy()
            if self.output_name is True:
                output_name = self._outname(ds_)
            else:
                output_name = self.output_name
            if not output_name:
                print("Could not write output.")
                continue
            outputname = Path(os.path.join(output_dir, output_name)).resolve()
            ds_dict[output_name] = self._to_netcdf(ds_, outputname)

    def _parse_components_to_format(self, ds, out_components, out_format):
        def test_ocomp(ocomp):
            return ocomp.replace("/", "")

        ocomps = []
        for comp in out_components:
            if hasattr(ds, comp):
                ocomps.append(test_ocomp(getattr(ds, comp)))
            elif hasattr(self.proc, comp):
                ocomps.append(test_ocomp(getattr(self.proc, comp)))
            elif hasattr(self.ds, comp):
                ocomps.append(test_ocomp(getattr(self.ds, comp)))
            else:
                ocomps.append("NA")
                warnings.warn(f"{comp} not found!")
        return out_format.format(*ocomps)

    def _outname(self, ds):
        """Set project-specific ouput file name."""

        try:
            output_fmt = pjson[self.project]["format"]
            output_comps = pjson[self.project]["components"].split(", ")
        except ValueError:
            warnings.warn(f"Project {self.project} not known")
            return
        return self._parse_components_to_format(ds, output_comps, output_fmt)

    def _directory_structure(self, ds):
        """Set project-specific directory structure."""
        try:
            output_fmt = pjson[self.project]["drs_format"]
            output_comps = pjson[self.project]["drs_components"].split(", ")
        except ValueError:
            warnings.warn(f"Project {self.project} not known")
            return
        return self._parse_components_to_format(ds, output_comps, output_fmt)

    def _to_netcdf(self, ds, name):
        """Write xarray.Dataset to netCDF file on disk."""
        ds = save_xrdataset(
            ds,
            name=name,
            encoding_dict={
                "encoding": {
                    self.CIname: {"dtype": "float32"},
                }
            },
        )
        print(f"File written: {name}")
        return ds
