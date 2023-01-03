import copy
import warnings

from . import _consts
from ._ci_netcdfattrs import NetCDFglobalattrs
from ._tables import ijson, xjson
from ._utils import (
    check_existance,
    get_time_range_as_str,
    kwargs_to_self,
    object_attrs_to_self,
)


class PostProcessing:
    """Class for post-processing ``index_calculator.processing`` object.

    Parameters
    ----------
    proc_obj: index_calculator.processing
        ``index_calculator.processing`` object
    project: {"CORDEX", "CMIP5", "CMIP6", "N/A"} (default: "N/A), optional
        Project name
    institution_id: str (default: "N/A"), optional
        Short name of the institution calculating the climate indicator.
    institution: str (default: "N/A"), optional
        Long name of the institution calculating the climate indicator.
    contact: str (default: "N/A"), optional
        Mail contact of the institution calculating the climate indicator.

    Example
    -------
    Calculate a climate indicator `TG` from netcdf file on disk
    and do some post-processing::

        from pyhomogenize import open_xrdataset
        from index_calculator import preprocessing
        from index_calculator import processing
        from index_calculator import postprocessing

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

        postproc_ds = postproc.postproc
    """

    def __init__(
        self,
        proc_obj=None,
        project="N/A",
        institution_id="N/A",
        institution="N/A",
        contact="N/A",
        split=True,
        **kwargs,
    ):
        if proc_obj is None:
            raise ValueError(
                "Select an index_calculator.Processing object. 'proc_obj=...'"
            )
        object_attrs_to_self(proc_obj, self)

        self.project = check_existance({"project": project}, self)
        self.institution_id = check_existance(
            {"institution_id": institution_id},
            self,
        )
        self.institution = check_existance(
            {"institution": institution},
            self,
        )
        self.contact = check_existance({"contact": contact}, self)
        self.period = check_existance({"period": False}, self)
        self.split = check_existance({"split": split}, self)
        kwargs_to_self(kwargs, self)
        self.postproc = self._postprocessing()

    def _get_time_borders(self, times):
        left, right = get_time_range_as_str(times, self.fmt)
        return "{}-{}".format(left, right)

    def _postprocessing(self):
        _ijson = copy.deepcopy(ijson)
        _xjson = copy.deepcopy(xjson)

        def adjust_attributes(dictionary, value):
            output = {}
            for key in dictionary.keys():
                if isinstance(dictionary[key], dict):
                    output[key] = adjust_attributes(dictionary[key], value)
                else:
                    output[key] = dictionary[key].format(**value)
            return output

        json = {}
        json[self.IDXname] = _ijson[self.IDXname]
        json["global_att"] = _xjson["global_att"]
        try:
            json["global_att"].update(_xjson[self.project]["global_att"])
        except KeyError:
            warnings.warn(f"Project {self.project} not known.")
        json = adjust_attributes(json, self.replacement)
        output = NetCDFglobalattrs(
            self,
            self.proc,
            json["global_att"],
        ).output
        for attr_name, attr_value in json[self.IDXname].items():
            output[self.CIname].attrs[attr_name] = attr_value
        associated_files = []
        for var_name in self.var_name:
            if "associated_files" not in self.ds[var_name].attrs.keys():
                continue
            assoc_files = self.ds[var_name].attrs["associated_files"]
            if isinstance(assoc_files, str):
                assoc_files = [assoc_files]
            for assoc_file in assoc_files:
                associated_files += [assoc_file]
        associated_files = ", ".join(associated_files)
        output[self.CIname].attrs["associated_files"] = associated_files
        if self.split is True:
            self.split = _consts._split[self.freq]
        trange = "ci_timerange_index"
        if self.split is False:
            output.attrs[trange] = self._get_time_borders(output.time.values)
            return output
        olist = []
        for name, ds in output.resample({"time": self.split}):
            ds_ = ds.copy()
            ds_.attrs[trange] = self._get_time_borders(ds.time.values)
            olist.append(ds_)
        return olist
