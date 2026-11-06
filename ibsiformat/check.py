from pathlib import Path


def check(path: Path | str):
    from ibsiformat.read import read_yaml_file
    from ibsiformat.utilities import flatten_yaml_dict

    # Read file.
    x = read_yaml_file(path=path)
    x = flatten_yaml_dict(x)

    # Build a json lookup table to be able to identify relevant json files.
    lut = build_json_lookup_table()

    pass


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
