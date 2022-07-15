import pytest  # noqa
from pyhomogenize import open_xrdataset

import index_calculator as xcalc
from index_calculator import test_netcdf


def test_processing():
    tas_ds = open_xrdataset(test_netcdf["tas"])
    preproc = xcalc.preprocessing(tas_ds, freq="week")
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
    tas_ds = open_xrdataset(test_netcdf["tas"])
    xcalc.index_calculator(
        ds=tas_ds,
        freq="week",
        index="TG",
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
    ).compute(write=True)


def test_thresh_index_calculator():
    pr_ds = open_xrdataset(test_netcdf["pr"])
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RX3day",
        project="CORDEX",
        institution_id="TEST",
    ).compute()
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RXYYday",
        thresh=3,
        project="CORDEX",
        institution_id="TEST",
    ).compute()
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RXYYday",
        project="CORDEX",
        institution_id="TEST",
    ).compute()
