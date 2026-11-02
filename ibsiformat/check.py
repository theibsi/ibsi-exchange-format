from pathlib import Path


def check(path: Path | str):
    # Read file.
    x = read_yaml_file(path = path)

    # Build a json lookup table to be able to identify relevant json files.

def read_yaml_file(path: Path | str) -> dict:
    import strictyaml

    # Attempt to read yaml file.
    if path is str:
        path = Path(path)
    elif path is not Path:
        raise TypeError(f"Path must be a Path object, but is {type(path)}.")
    if not path.is_file():
        raise FileNotFoundError(f"File {path} does not exist.")
    if path.suffix not in [".yml", ".yaml"]:
        raise FileNotFoundError(f"File {path} is not a YAML file.")

    # Read YAML file. Note that we do not enforce a scheme at this point.
    with open(path, "r", encoding="utf-8") as f:
        x = strictyaml.dirty_load(f.read(), allow_flow_style=True)

    return x

def build_json_lookup_table():
    # Build json look-up table to facilitate building validators or templator.
    from importlib.resources import files
    import ibsiformat

    json_files = files(ibsiformat.json_data)