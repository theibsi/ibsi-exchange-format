import os.path
from pathlib import Path

CURRENT_DIR = os.path.dirname(__file__)

def test_format_check():
    from ibsiformat.check import check

    check(path = Path(os.path.join(CURRENT_DIR, "yaml", "example.yaml")))
