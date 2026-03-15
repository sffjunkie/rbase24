from typing import NamedTuple

from rich.console import Console
from rbase24.typedefs import SchemeDB


class Context(NamedTuple):
    console: Console
    db: SchemeDB
