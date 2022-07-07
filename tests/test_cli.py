import pytest  # noqa

import index_calculator as xcalc
from index_calculator import test_netcdf


def test_cli():
    parser = xcalc.cli._parser()
    args = parser.parse_args(
        [
            "-i",
            test_netcdf,
            "-o",
            "test.nc",
            "-x",
            "TG",
            "-p",
            "CORDEX",
            "-inst",
            "test_institution",
            "-inst_id",
            "TEST",
            "-contact",
            "test@test.de",
            "-freq",
            "week",
        ]
    )
    xcalc.cli._args_to_xcalc(args)
