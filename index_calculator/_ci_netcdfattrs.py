from datetime import datetime as dt

import xclim as xc


class NetCDFattrs:
    """Class for writing key-value pairs to netCDF attributes."""

    def vanish_dictionary(self, dictionary):
        """Delete non-default key-value pairs from dictionary.

        Default key-value pairs are marked with '<'
        at the beginning of the value.

        Parameters
        ----------
        dictionary :  dict

        Returns
        -------
        dict,
            Dictionary with deleted non-default key-value pairs.
        """
        new_dictionary = {}
        for key, value in dictionary.items():
            if value and value[0] != "<":
                new_dictionary[key] = value
        return new_dictionary

    def write_dictionary_to_netcdf(self, database, dictionary):
        """Write key-value pairs to netCDF attributes.

        Parameters
        ----------
        database : xarray.Dataset or xarray.DataArray
            The key-value pairs will be written to the `database` attributes.
        dictionary: dict
            Dictionary with key-value pairs.

        Returns
        -------
        xarray.Dataset or xarray.DataArray
            Database with new attributes
        """
        for k, v in dictionary.items():
            database.attrs[k] = v
        return database


class NetCDFvariableattrs(NetCDFattrs):
    """Class for writing key-value pairs to xarray.DataArray attributes."""

    def __init__(self, postproc, da, dictionary={}):
        """Write key-value-pairs to xarray.DataArray attributes.

        Parameters
        ----------
        postproc: PostProcessing
            index_calculator PostProcessing object
        da: xarray.DataArray
            The key-value pairs will be written to the `da` attributes
        dictionary: dict, optional
            Dictionary with key-value pairs.

        Returns
        -------
        xarray.DataArray
            Database with new attributes
        """
        dictionary = {**dictionary, **self._associated_files(object)}
        dictionary = self.vanish_dictionary(dictionary)
        return self.write_dictionary_to_netcdf(da, dictionary)

    def _associated_files(self, input):
        """Write associated files to attributes."""
        return {"associated_files": "test"}


class NetCDFglobalattrs(NetCDFattrs):
    """Class for writing key-value pairs to xarray.Dataset attributes."""

    def __init__(self, postproc, ds, dictionary={}):
        """Write key-value-pairs to xarray.Dataset attributes.

        Parameters
        ----------
        postproc: PostProcessing
            index_calculator PostProcessing object
        ds: xarray.Dataset
            The key-value pairs will be written to the `ds` attributes
        dictionary: dict, optional
            Dictionary with key-value pairs.

        Returns
        -------
        xarray.Dataset
            Database with new attributes
        """
        dictionary = {
            **dictionary,
            **self._ci_additional_reference_period(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_creation_date(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_institute_id(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_institution(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_contact(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_name(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_reference_period(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_frequency(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_timerange_index(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_timerange_source(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_package_name(postproc),
        }
        dictionary = {
            **dictionary,
            **self._ci_package_reference(postproc),
        }
        dictionary = self.vanish_dictionary(dictionary)
        return self.write_dictionary_to_netcdf(ds, dictionary)

    def _ci_additional_reference_period(self, input):
        """Add additional reference period to dictionary."""
        return {"ci_additional_reference_period": input.period}

    def _ci_creation_date(self, input):
        """Add creation date to dictionary."""
        return {"ci_creation_date": dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")}

    def _ci_institution(self, input):
        """Add institution long name to dictionary."""
        return {"ci_institution": input.institution}

    def _ci_institute_id(self, input):
        """Add institution short name to dictionary."""
        return {"ci_institute_id": input.institution_id}

    def _ci_contact(self, input):
        """Add contact to dictionary."""
        return {"ci_contact": input.contact}

    def _ci_name(self, input):
        """Add climate index name to dictionary."""
        return {"ci_name": input.CIname}

    def _ci_package_reference(self, input):
        """Add index_calculator version to dictionary."""
        return {"ci_package_reference": "xcalc_v0.1.0"}

    def _ci_package_name(self, input):
        """Add xclim version to dictionary."""
        return {"ci_package_name": f"xclim_{xc.__version__}"}

    def _ci_reference_period(self, input):
        """Add reference period to dictionary."""
        return {"ci_reference_period": input.base_period_time_range}

    def _ci_frequency(self, input):
        """Add frequency to dictionary."""
        return {"ci_frequency": input.freq}

    def _ci_timerange_index(self, input):
        """Add time range of the index to dictionary."""
        tstr = f"{input.TimeRange[0]}-{input.TimeRange[1]}"
        return {"ci_timerange_index": tstr}

    def _ci_timerange_source(self, input):
        """Add time range of the source to dictionary."""
        atstr = f"{input.ATimeRange[0]}-{input.ATimeRange[1]}"
        return {"ci_timerange_source": atstr}
