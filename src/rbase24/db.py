from pathlib import Path

import yaml
import slugify
from rbase24.typedefs import ColorScheme, SchemeDB, Palette, SchemeKeys


def load_scheme(scheme_file: Path) -> ColorScheme:
    with open(scheme_file, "r") as fp:
        data = yaml.load(fp.read(-1), yaml.SafeLoader)

        palette_data = data.get("palette", None)
        if palette_data is None:
            raise ValueError(
                f"Scheme file {scheme_file} must contain a 'palette' entry"
            )

        palette: Palette = {k: v.lower() for k, v in palette_data.items()}  # type: ignore

        system = data.get(SchemeKeys.SYSTEM, None)
        if system is None:
            if len(palette) == 16:
                system = "base16"
            else:
                system = "base24"

        slug = data.get(SchemeKeys.SLUG, None)
        if slug is None:
            slug = slugify.slugify(scheme_file.stem)

        description = data.get(SchemeKeys.DESCRIPTION, "")
        variant = data.get(SchemeKeys.VARIANT, "unknown")

        return ColorScheme(
            file=scheme_file.name,
            scheme=data["name"],
            author=data["author"],
            system=system,
            slug=slug,
            description=description,
            variant=variant,
            palette=palette,
        )


def load(scheme_dir: Path) -> SchemeDB:
    print(scheme_dir)
    if not scheme_dir.exists():
        return {}

    return {
        scheme_file.name: load_scheme(scheme_file)
        for scheme_file in scheme_dir.glob("**/*.yaml")
    }


def list_schemes(db: SchemeDB) -> list[str]:
    return [key for key in db.keys()]
