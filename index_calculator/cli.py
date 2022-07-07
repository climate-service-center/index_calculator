"""Console script for index_calculator."""
import argparse
import sys

import dask  # noqa
from dask.distributed import Client
from pyhomogenize import open_xrdataset

import index_calculator as xcalc


def _parser():
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
    return parser.parse_args()


def main():

    args = _parser()

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
