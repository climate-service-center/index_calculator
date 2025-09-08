import importlib.resources as resources
import json


def read_from_json(jsfile):
    """Read json file from package resources.

    Parameters
    ----------
    jsfile: str
        Json file path relative to the package.

    Returns
    -------
    dict
       Python dictionary.
    """
    with (
        resources.files("index_calculator")
        .joinpath(jsfile)
        .open("r", encoding="utf-8") as f
    ):
        return json.load(f)


mjson = read_from_json("tables/metadata.json")
xjson = read_from_json("tables/xcalc.json")
pjson = read_from_json("tables/projects.json")
vjson = read_from_json("tables/input_vars.json")
cfjson = read_from_json("tables/cf_conversion.json")
fjson = read_from_json("tables/convert_to_frequency.json")
