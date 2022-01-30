import json

from typing import Dict, List, Union


def read_file_content(file_path: str) -> str:
    return open(file_path).read()


def read_json(file_path: str) -> Union[List, Dict]:
    return json.loads(read_file_content(file_path))
