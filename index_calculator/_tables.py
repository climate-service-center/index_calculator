import json

import pkg_resources


def read_from_json(jsfile):
    """Read json file from disk.

    Parameters
    ----------
    jsfile: str
        Json file on disk.

    Returns
    -------
    dict
       Python dictionary.
    """
    with pkg_resources.resource_stream("index_calculator", jsfile) as f:
        return json.load(f)


ijson = read_from_json("tables/indices.json")
xjson = read_from_json("tables/xcalc.json")
pjson = read_from_json("tables/projects.json")
vjson = read_from_json("tables/input_vars.json")
