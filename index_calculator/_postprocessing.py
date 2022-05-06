import warnings

from ._ci_netcdfattrs import NetCDFglobalattrs, NetCDFvariableattrs
from ._tables import ijson, xjson
from ._utils import object_attrs_to_self


class PostProcessing:
    def __init__(
        self,
        project=None,
        institution=None,
        institution_id=None,
        proc_obj=None,
        **kwargs,
    ):

        if project is None:
            raise ValueError("Please select a project name. 'project=...'")
        if institution is None:
            raise ValueError(
                "Please select an institution short name. 'institution=...'"
            )
        if institution_id is None:
            raise ValueError(
                "Please select an institution long name, 'insutution_id=...'"
            )

        self.project = project
        self.institution = institution
        self.institution_id = institution_id

        self.period = None
        self.base_period_time_range = None

        if proc_obj is not None:
            object_attrs_to_self(proc_obj, self)
        self.postproc = self.postprocessing()

    def postprocessing(self):
        def adjust_attributes(dictionary, value):
            output = {}
            for key in dictionary.keys():
                if isinstance(dictionary[key], dict):
                    output[key] = adjust_attributes(dictionary[key], value)
                else:
                    output[key] = dictionary[key].format(value)
            return output

        json = {}
        json[self.CIname] = ijson[self.CIname]
        json[self.CIname].update(xjson["variable_att"])
        json["global_att"] = xjson["global_att"]
        try:
            json["global_att"].update(xjson[self.project]["global_att"])
        except ValueError:
            warnings.warn(f"Project {self.project} not known.")
        self.json = adjust_attributes(json, None)

        output = NetCDFvariableattrs(
            self, self.proc[self.CIname], self.json[self.CIname]
        ).output
        output = NetCDFglobalattrs(
            self,
            self.proc,
            self.json["global_att"],
        ).output

        return output
