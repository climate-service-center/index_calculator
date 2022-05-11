"""Console script for index_calculator."""
import argparse
import sys

import dask  # noqa
import xarray as xr
from dask.distributed import Client

import index_calculator as xcalc


def open_xrdataset(
    files,
    use_cftime=True,
    parallel=True,
    data_vars="minimal",
    chunks={"time": 1},
    coords="minimal",
    compat="override",
    drop=None,
    **kwargs,
):
    """optimized function for opening large cf datasets.
    based on:
    https://github.com/pydata/xarray/issues/1385#issuecomment-561920115
    decode_timedelta=False is added to leave variables and coordinates
    with time units in {“days”, “hours”, “minutes”, “seconds”,
    “milliseconds”, “microseconds”} encoded as numbers.
    """

    def drop_all_coords(ds):
        return ds.reset_coords(drop=True)

    ds = xr.open_mfdataset(
        files,
        parallel=parallel,
        decode_times=False,
        combine="by_coords",
        preprocess=drop_all_coords,
        decode_cf=False,
        chunks=chunks,
        data_vars=data_vars,
        coords=coords,
        compat=compat,
        **kwargs,
    )

    return xr.decode_cf(ds, use_cftime=use_cftime, decode_timedelta=False)


def main():
    """Console script for index_calculator."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_file",
        dest="input_file",
        nargs="?",
        help="netCDF input file name",
    )
    parser.add_argument(
        "-x",
        "--index",
        dest="climate_index",
        nargs="?",
        help="climate index short name",
    )
    parser.add_argument(
        "-p",
        "--project",
        dest="project",
        default="N/A",
        help="MIP project name",
    )
    parser.add_argument(
        "-inst",
        "--institute",
        dest="institution",
        default="N/A",
        help="institution name",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        default=True,
        help="netCDF output file name. Necessary if project is not selected.",
    )
    args = parser.parse_args()

    ds = open_xrdataset(args.input_file)
    xcalc.index_calculator(
        ds=ds,
        index=args.climate_index,
        project=args.project,
        institution_id=args.institution,
        output=args.output,
    ).compute(write=True)
    return 0


if __name__ == "__main__":
    with Client() as client:
        sys.exit(main())  # pragma: no cover
