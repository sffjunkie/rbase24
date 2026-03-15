import typer
from rich.console import Console

from rbase24.cli import listing, show
from rbase24.config import Base24ViewerConfig
from rbase24.context import Context
from rbase24.db import load

app = typer.Typer()


@app.callback()
def main(
    ctx: typer.Context,
):
    cfg = Base24ViewerConfig()
    if cfg.scheme_dir is None or not cfg.scheme_dir.exists():
        print("No base16 scheme directory configured. Exiting")
        return

    db = load(cfg.scheme_dir)
    if not db:
        print(f"No schemes found in {cfg.scheme_dir}")

    context = Context(
        console=Console(),
        db=db,
    )

    ctx.obj = {}
    ctx.obj["context"] = context


app.add_typer(listing.app)
app.add_typer(show.app)
