import os

import pytest  # noqa

from index_calculator import test_netcdf


def test_cli():
    s = (
        "index_calculator "
        "-i {} "
        "-o test.nc "
        "-x TG "
        "-p CORDEX "
        "-inst test_institution "
        "-inst_id TEST "
        "-contact test@test.de "
        "-freq week"
    ).format(test_netcdf)
    os.system(s)
