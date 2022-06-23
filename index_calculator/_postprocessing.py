import copy
import warnings

from ._ci_netcdfattrs import NetCDFglobalattrs, NetCDFvariableattrs
from ._tables import ijson, istjson, xjson
from ._utils import check_existance, kwargs_to_self, object_attrs_to_self


class PostProcessing:
    """Class for post-precessing."""

    def __init__(
        self,
        project="N/A",
        institution_id="N/A",
        institution="N/A",
        contact="N/A",
        proc_obj=None,
        **kwargs,
    ):
        """Write parameters to self."""
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
        if self.institution_id in istjson.keys():
            info = istjson[self.institution_id]
            if self.institution == "N/A":
                self.institution = info["institution_long_name"]
            if self.contact == "N/A":
                self.contact = info["institution_contact"]

        self.period = check_existance({"period": False}, self)
        self.base_period_time_range = check_existance(
            {"base_period_time_range": False}, self
        )

        kwargs_to_self(kwargs, self)
        self.postproc = self.postprocessing()

    def postprocessing(self):
        """Write key-value pairs to netCDF attributes."""
        _ijson = copy.deepcopy(ijson)
        _xjson = copy.deepcopy(xjson)

        def adjust_attributes(dictionary, value):
            output = {}
            for key in dictionary.keys():
                if isinstance(dictionary[key], dict):
                    output[key] = adjust_attributes(dictionary[key], value)
                else:
                    output[key] = dictionary[key].format(value)
            return output

        json = {}
        json[self.CIname] = _ijson[self.CIname]
        json[self.CIname].update(_xjson["variable_att"])
        json["global_att"] = _xjson["global_att"]
        try:
            json["global_att"].update(_xjson[self.project]["global_att"])
        except KeyError:
            warnings.warn(f"Project {self.project} not known.")
        json = adjust_attributes(json, None)
        output = NetCDFvariableattrs(
            self,
            self.proc[self.CIname],
            json[self.CIname],
        )
        output = NetCDFglobalattrs(
            self,
            self.proc,
            json["global_att"],
        )

        return output
