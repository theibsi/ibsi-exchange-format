from pathlib import Path


def check(path: Path | str):
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

    with open(path, "r", encoding="utf-8") as f:
        x = strictyaml.dirty_load(f.read(), allow_flow_style=True)


def build_json_lookup_table():
    # Build json look-up table to facilitate building validators or templator.
    from importlib.resources import files
    import ibsiformat

    json_files = files(ibsiformat.json_data)