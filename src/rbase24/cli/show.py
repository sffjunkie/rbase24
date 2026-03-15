from operator import itemgetter
from itertools import islice
from math import floor
from typing import Annotated, Iterable

import typer
from rich import box
from rich.console import Console, group
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from rbase24.color import contrast_color, hex_string_to_rgb
from rbase24.typedefs import Palette, ColorScheme, SchemeKeys


def print_schemes(filtered_schemes: list[ColorScheme]) -> None:
    console = Console()
    column_count = int(floor(console.width / 54))

    table = Table.grid(padding=0)
    for col in range(column_count):
        table.add_column(str(col))

    chunks = [batch for batch in chunked(filtered_schemes, column_count)]

    for schemes in chunks:
        panels = []
        for scheme in schemes:
            panels.append(
                Panel(
                    SchemeHeader(scheme),
                    width=50,
                    box=box.MINIMAL,
                )
            )
        table.add_row(*panels)

    console.print(table)


@group()
def SchemeHeader(scheme: dict):
    yield Text(f"Scheme: {scheme[SchemeKeys.SCHEME]}")
    yield Text(f"Author: {scheme[SchemeKeys.AUTHOR]}")
    yield Text(f"Slug: {scheme[SchemeKeys.SLUG]}")
    yield Text(f"File: {scheme[SchemeKeys.FILE]}")
    yield Text(f"System: {scheme[SchemeKeys.SYSTEM]}")

    if scheme["description"]:
        yield Text(f"Description: {scheme[SchemeKeys.DESCRIPTION]}")

    yield Panel(
        SchemePalette(scheme["palette"]),
        box=box.MINIMAL,
    )


@group()
def SchemePalette(palette: Palette):
    table = Table.grid(padding=1)
    table.add_column("0")
    table.add_column("2")
    table.add_column("3")
    table.add_column("4")

    chunks = [batch for batch in chunked(palette.items(), 4)]

    for chunk in chunks:
        items = []
        for name, value in chunk:
            if not value[0] == "#":
                value = f"#{value}"
            rgb = hex_string_to_rgb(value)
            contrast = contrast_color(rgb)
            style = Style(color=contrast, bgcolor=value)

            display_name = f"{name:^10}"
            display_value = f"{value:^10}"
            items.append(Text(f"\n{display_name}\n{display_value}\n", style=style))
        table.add_row(*items)

    yield table


def chunked(iterable, n) -> Iterable:
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


app = typer.Typer()


@app.command()
def show(
    ctx: typer.Context,
    spec: Annotated[str, typer.Argument()] = "*",
    key: Annotated[
        SchemeKeys,
        typer.Option(
            "--key",
            "-k",
            help="Filter by key type.",
            metavar="KEY",
        ),
    ] = SchemeKeys.FILE,
):
    """Show Schemes"""
    if spec is None:
        spec = "*"

    db = ctx.obj["context"].db

    get_by = key.value
    values = db.values()
    if spec != "*":
        filtered_data = filter(
            lambda item: item[get_by].lower().find(spec.lower()) != -1, values
        )
    else:
        filtered_data = values

    if get_by != "file":
        sort_key = itemgetter(get_by, "file")
    else:
        sort_key = itemgetter("file")

    sorted_data = sorted(filtered_data, key=sort_key)

    print_schemes(sorted_data)
