import pytest  # noqa
from pyhomogenize import open_xrdataset

import index_calculator as xcalc
from index_calculator import test_netcdf


def test_processing():
    tas_ds = open_xrdataset(test_netcdf)
    preproc = xcalc.preprocessing(tas_ds)
    proc = xcalc.processing("TG", preproc_obj=preproc)
    postproc = xcalc.postprocessing(
        "CORDEX",
        proc_obj=proc,
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
    )
    xcalc.outputwriter(postproc_obj=postproc).write_to_netcdf()


def test_index_calculator():
    tas_ds = open_xrdataset(test_netcdf)
    xcalc.index_calculator(
        ds=tas_ds,
        index="TG",
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
    ).compute(write=True)
