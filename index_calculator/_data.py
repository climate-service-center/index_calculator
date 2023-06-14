from pathlib import Path

data_path = Path(__file__).parent

nclist_tas_hour = list((data_path / "data").glob("tas_*1hr*"))
nclist_tas_day = list((data_path / "data").glob("tas_*day*"))
nclist_pr_day = list((data_path / "data").glob("pr_*day*"))

netcdf_tas_hour = [nc.as_posix() for nc in nclist_tas_hour]
netcdf_tas_day = [nc.as_posix() for nc in nclist_tas_day][0]
netcdf_pr_day = [nc.as_posix() for nc in nclist_pr_day][0]
netcdf = {
    "tas": {
        "1hr": netcdf_tas_hour,
        "day": netcdf_tas_day,
    },
    "pr": {
        "day": netcdf_pr_day,
    },
}
