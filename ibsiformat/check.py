import copy
from copy import deepcopy
from functools import lru_cache
from pathlib import Path


def check(path: Path | str):
    # Read file.
    x = read_yaml_file(path=path)

    # Build a json lookup table to be able to identify relevant json files.
    lut = build_json_lookup_table()

    if "imaging" in x:
        ...

    if "features" in x:
        y = flatten_features(x)
    pass


def flatten_features(x):

    def merge_shared_attributes(feature, shared_attributes):
        return {**shared_attributes, **feature}

    def process_featureset(featureset, shared_attributes):
        for feature in featureset:
            if isinstance(feature, dict):
                if 'features' in feature:
                    features = feature['features']
                    for sub_feature in features:
                        sub_feature = merge_shared_attributes(sub_feature, shared_attributes)
                        flattened_features.append(sub_feature)
                else:
                    feature = merge_shared_attributes(feature, shared_attributes)
                    flattened_features.append(feature)
            else:
                flattened_features.append(feature)

    y = copy.deepcopy(x)

    for key, value in x.items():
        if key != "features":
            continue

        if isinstance(value, list):
            for entry in value:
                ...

    return y



def read_yaml_file(path: Path | str) -> dict:
    import strictyaml

    # Attempt to read yaml file.
    if isinstance(path, str):
        path = Path(path)
    elif not isinstance(path, Path):
        raise TypeError(f"Path must be a Path object, but is {type(path)}.")
    if not path.is_file():
        raise FileNotFoundError(f"File {path} does not exist.")
    if path.suffix not in [".yml", ".yaml"]:
        raise FileNotFoundError(f"File {path} is not a YAML file.")

    # Read YAML file. Note that we do not enforce a scheme at this point.
    with open(path, "r", encoding="utf-8") as f:
        x = strictyaml.dirty_load(f.read(), allow_flow_style=True).data

    return x



class LookupTable:
    def __init__(self, json_data: list[dict[str, str]]):
        self.name: list[str] = [x["name"] for x in json_data]
        self.ibsi_id: list[str | None] = [x["ibsi-id"] if "ibsi-id" in x else None for x in json_data]

        # Dictionaries containing json data.
        self.json = json_data

    def get(self, name=None, ibsi_id=None) -> dict[str, str]:
        """
        Lookup table for attribute dicts. Attribute dicts can be looked up using either their name, or their IBSI
        identifier. if any.

        :param name: name of an attribute.
        :param ibsi_id: 4-character ibsi-id of an attribute.
        :return: attribute dict corresponding for the name or provided IBSI identifier.
        """

        if name is not None:
            ii = self.name.index(name)
            return self.json[ii]
        elif ibsi_id is not None:
            ii = self.ibsi_id.index(ibsi_id)
            return self.json[ii]
        else:
            raise ValueError("Either name or ibsi_id must be provided.")


def build_json_lookup_table() -> LookupTable:
    # Build json look-up table to facilitate building validators or templator.
    from importlib.resources import files
    import ibsiformat
    import json

    json_list = []
    for json_file in files(ibsiformat).joinpath("json_data").iterdir():
        json_list += [json.loads(json_file.read_text(encoding="utf-8"))]

    lut = LookupTable(json_list)

    return lut
