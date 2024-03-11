import os

import pytest  # noqa

from .conftest import tas_day_netcdf


def test_cli():
    s = (
        "index_calculator "
        f"-i {tas_day_netcdf()} "
        "-o test.nc "
        "-x TG "
        "-p CORDEX "
        "-inst test_institution "
        "-inst_id TEST "
        "-contact test@test.de "
        "-freq week"
    )
    os.system(s)
