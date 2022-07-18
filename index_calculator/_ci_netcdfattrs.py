import warnings
from datetime import datetime as dt

import xclim as xc

from index_calculator import __version__


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
            if not value:
                continue
            if value[0] == "<":
                continue
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
        dictionary = self._create_dictionary(
            list_of_attributes=[
                "ci_additional_reference_period",
                "ci_creation_date",
                "ci_institute_id",
                "ci_institution",
                "ci_contact",
                "ci_name",
                "ci_reference_period",
                "ci_frequency",
                "ci_timerange_index",
                "ci_timerange_source",
                "ci_package_name",
                "ci_package_reference",
            ],
            obj=postproc,
        )
        dictionary = self.vanish_dictionary(dictionary)
        self.output = self.write_dictionary_to_netcdf(ds, dictionary)

    def _create_dictionary(self, list_of_attributes, obj):
        """Create attributes dictionary."""
        dictionary = {}
        for attribute in list_of_attributes:
            try:
                dictionary[attribute] = getattr(self, "_" + attribute)(obj)
            except AttributeError:
                warnings.warn("Could not set attribute {}".format(attribute))
        return dictionary

    def _ci_additional_reference_period(self, obj):
        """Add additional reference period to dictionary."""
        return obj.period

    def _ci_creation_date(self, obj):
        """Add creation date to dictionary."""
        return dt.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def _ci_institution(self, obj):
        """Add institution long name to dictionary."""
        return obj.institution

    def _ci_institute_id(self, obj):
        """Add institution short name to dictionary."""
        return obj.institution_id

    def _ci_contact(self, obj):
        """Add contact to dictionary."""
        return obj.contact

    def _ci_name(self, obj):
        """Add climate index name to dictionary."""
        return obj.CIname

    def _ci_package_reference(self, obj):
        """Add index_calculator version to dictionary."""
        return f"xcalc_{__version__}"

    def _ci_package_name(self, obj):
        """Add xclim version to dictionary."""
        return f"xclim_{xc.__version__}"

    def _ci_reference_period(self, obj):
        """Add reference period to dictionary."""
        start = obj.base_period_time_range[0]
        end = obj.base_period_time_range[1]
        return f"{start}-{end}"

    def _ci_frequency(self, obj):
        """Add frequency to dictionary."""
        return obj.freq

    def _ci_timerange_index(self, obj):
        """Add time range of the index to dictionary."""
        return f"{obj.TimeRange[0]}-{obj.TimeRange[1]}"

    def _ci_timerange_source(self, obj):
        """Add time range of the source to dictionary."""
        return f"{obj.ATimeRange[0]}-{obj.ATimeRange[1]}"
