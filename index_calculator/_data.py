from pathlib import Path

data_path = Path(__file__).parent

nclist = list((data_path / "data").glob("*"))
netcdf = [nc.as_posix() for nc in nclist][0]
