from itertools import islice
from typing import Optional

import typer
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text
from typing_extensions import Annotated

from rbase24.scheme import load_schemes
from rbase24.typedefs import Palette, SchemeDB
from rbase24.color import hex_string_to_rgb, contrast_color
from rbase24.config import Base24ViewerConfig


def print_schemes(db: SchemeDB):
    console = Console()
    for name, scheme in db.items():
        console.print(f"Name: {scheme['name']}")
        console.print(f"Author: {scheme['author']}")
        console.print(f"File: {name}")
        console.print(f"Slug: {scheme['slug']}")
        console.print(f"System: {scheme['system']}")

        if scheme["description"]:
            console.print(f"Description: {scheme['description']}")

        console.print()
        print_palette(scheme["palette"])
        console.print()


def chunked(iterable, n):
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def print_palette(palette: Palette):
    console = Console()
    table = Table.grid(padding=1)
    table.add_column("0")
    table.add_column("2")
    table.add_column("3")
    table.add_column("4")

    chunks = [batch for batch in chunked(palette.items(), 4)]

    for chunk in chunks:
        items = []
        for name, value in chunk:
            rgb = hex_string_to_rgb(f"#{value}")
            contrast = contrast_color(rgb)

            style = Style(color=contrast, bgcolor=f"#{value}")
            items.append(Text(f"\n {name} \n #{value} \n", style=style))
        table.add_row(*items)
    console.print(table)
    console.print()


def go(filespec: Annotated[Optional[str], typer.Argument()] = "*"):
    cfg = Base24ViewerConfig()
    db = load_schemes(cfg.scheme_dir, filespec)
    if not db:
        if filespec == "*":
            print(f"No schemes found in {cfg.scheme_dir}")
        else:
            print(f"No schemes matching '{filespec}' found in {cfg.scheme_dir}")
        return
    print_schemes(db)


def main():
    typer.run(go)
