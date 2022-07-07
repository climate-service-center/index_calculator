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
        "-freq",
        "--frequency",
        dest="frequency",
        default="year",
        help="output file frequency",
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
        help="institution long name",
    )
    parser.add_argument(
        "-inst_id",
        "--institute_id",
        dest="institution_id",
        default="N/A",
        help="institution id",
    )
    parser.add_argument(
        "-contact",
        "--contact",
        dest="contact",
        default="N/A",
        help="institution mail contact",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        default=True,
        help="netCDF output file name. Necessary if project is not selected.",
    )
    return parser


def _args_to_xcalc(args):
    ds = open_xrdataset(args.input_file)
    return xcalc.index_calculator(
        ds=ds,
        index=args.climate_index,
        freq=args.frequency,
        project=args.project,
        institution=args.institution,
        institution_id=args.institution_id,
        contact=args.contact,
        output=args.output,
    ).compute(write=True)


def main():

    parser = _parser()
    args = parser.parse_args()

    _args_to_xcalc(args)
    return 0


if __name__ == "__main__":
    with Client() as client:
        sys.exit(main())  # pragma: no cover
