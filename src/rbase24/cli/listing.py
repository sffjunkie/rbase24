from typing_extensions import Annotated
from operator import itemgetter
import typer

from rich.table import Table

from rbase24.typedefs import SchemeDB, SchemeKeys

app = typer.Typer()


@app.command()
def ls(
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
    """List Schemes"""
    console = ctx.obj["context"].console
    db: SchemeDB = ctx.obj["context"].db

    tbl = Table(
        "Filename",
        "Title",
        "Variant",
        "System",
        header_style="green",
    )

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

    for scheme in sorted_data:
        tbl.add_row(
            scheme["file"],
            scheme["scheme"],
            scheme["variant"],
            scheme["system"],
        )

    console.print(tbl)
