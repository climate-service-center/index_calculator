from pathlib import Path

data_path = Path(__file__).parent

nclist_tas = list((data_path / "data").glob("tas_*"))
nclist_pr = list((data_path / "data").glob("pr_*"))
netcdf_tas = [nc.as_posix() for nc in nclist_tas][0]
netcdf_pr = [nc.as_posix() for nc in nclist_pr][0]
netcdf = {
    "tas": netcdf_tas,
    "pr": netcdf_pr,
}
