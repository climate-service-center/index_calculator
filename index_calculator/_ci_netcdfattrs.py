from datetime import datetime as dt

import xclim as xc


class NetCDFattrs:
    def vanish_dictionary(self, dictionary):
        new_dictionary = {}
        for key, value in dictionary.items():
            if value and value[0] != "<":
                new_dictionary[key] = value
        return new_dictionary

    def write_dictionary_to_netcdf(self, object, dictionary):
        for k, v in dictionary.items():
            object.attrs[k] = v
        return object


class NetCDFvariableattrs(NetCDFattrs):
    def __init__(self, object, basics, dictionary={}):
        dictionary = {**dictionary, **self._associated_files(object)}
        dictionary = self.vanish_dictionary(dictionary)
        self.output = self.write_dictionary_to_netcdf(basics, dictionary)

    def _associated_files(self, input):

        return {"associated_files": "test"}


class NetCDFglobalattrs(NetCDFattrs):
    def __init__(self, object, basics, dictionary={}):
        dictionary = {
            **dictionary,
            **self._ci_additional_reference_period(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_creation_date(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_institute_id(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_name(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_reference_period(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_frequency(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_timerange_index(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_timerange_source(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_package_name(object),
        }
        dictionary = {
            **dictionary,
            **self._ci_package_reference(object),
        }
        dictionary = self.vanish_dictionary(dictionary)
        self.output = self.write_dictionary_to_netcdf(basics, dictionary)

    def _ci_additional_reference_period(self, input):
        return {"ci_additional_reference_period": input.period}

    def _ci_creation_date(self, input):
        return {"ci_creation_date": dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")}

    def _ci_institution(self, input):
        return {"ci_institution": input.institution}

    def _ci_institute_id(self, input):
        return {"ci_institute_id": input.institution_id}

    def _ci_name(self, input):
        return {"ci_name": input.CIname}

    def _ci_package_reference(self, input):
        return {"ci_package_reference": "xcalc_v0.1.0"}

    def _ci_package_name(self, input):
        return {"ci_package_name": f"xclim_{xc.__version__}"}

    def _ci_reference_period(self, input):
        return {"ci_reference_period": input.base_period_time_range}

    def _ci_frequency(self, input):
        return {"ci_frequency": input.freq}

    def _ci_timerange_index(self, input):
        tstr = f"{input.TimeRange[0]}-{input.TimeRange[1]}"
        return {"ci_timerange_index": tstr}

    def _ci_timerange_source(self, input):
        atstr = f"{input.ATimeRange[0]}-{input.ATimeRange[1]}"
        return {"ci_timerange_source": atstr}
