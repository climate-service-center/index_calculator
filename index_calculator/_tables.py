import json

import pkg_resources


def read_from_json(jsfile):
    with pkg_resources.resource_stream("index_calculator", jsfile) as f:
        return json.load(f)


ijson = read_from_json("../tables/indices.json")
xjson = read_from_json("../tables/xcalc.json")
pjson = read_from_json("../tables/projects.json")
