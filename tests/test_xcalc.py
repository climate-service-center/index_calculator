import numpy as np  # noqa
import pyhomogenize as pyh  # noqa
import pytest  # noqa
import xarray as xr  # noqa
from pyhomogenize import open_xrdataset

import index_calculator as xcalc
from index_calculator import test_netcdf

from .conftest import tas_series, tasmax_series, tasmin_series  # noqa


def test_processing():
    tas_ds = open_xrdataset(test_netcdf["tas"]["day"])
    preproc = xcalc.preprocessing(
        tas_ds,
        freq="week",
        crop_time_axis=False,
        project="CORDEX",
    )
    proc = xcalc.processing("TG", preproc_obj=preproc)
    postproc = xcalc.postprocessing(
        proc_obj=proc,
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
    )
    xcalc.outputwriter(postproc_obj=postproc)


def test_index_calculator():
    tas_ds = open_xrdataset(test_netcdf["tas"]["day"])
    xcalc.index_calculator(
        ds=tas_ds,
        freq="week",
        index="TG",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
    )


def test_thresh_index_calculator():
    pr_ds = open_xrdataset(test_netcdf["pr"]["day"])
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RX3day",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
    )
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RXYYday",
        thresh=3,
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
    )
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RXYYday",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
    )


def test_perc_index_calculator():
    pr_ds = open_xrdataset(test_netcdf["pr"]["day"])
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="RR95p",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
        base_period_time_range=["2001-01-01", "2001-01-07"],
    )
    xcalc.index_calculator(
        ds=pr_ds,
        freq="week",
        index="R95p",
        crop_time_axis=False,
        project="CORDEX",
        institution_id="TEST",
        base_period_time_range=["2001-01-01", "2001-01-07"],
    )


def test_index_calculator_1hr():
    tas_ds = open_xrdataset(test_netcdf["tas"]["1hr"])
    xcalc.index_calculator(
        ds=tas_ds,
        freq="week",
        index="TG",
        crop_time_axis=False,
        project="CORDEX",
        institution="test institution",
        institution_id="TEST",
        contact="test@test.de",
        write=True,
    )
