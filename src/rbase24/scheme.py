import os
from pathlib import Path

import yaml
import slugify
from rbase24.typedefs import ColorScheme, SchemeDB
from rbase24.config import Base24ViewerConfig


def load_scheme(scheme_file: Path) -> ColorScheme:
    with open(scheme_file, "r") as fp:
        data = yaml.load(fp.read(-1), yaml.SafeLoader)

        palette = data.get("palette", None)
        if palette is None:
            raise ValueError(
                f"Scheme file {scheme_file} must contain a 'palette' entry"
            )

        system = data.get("system", None)
        if system is None:
            if len(palette) == 16:
                system = "base16"
            else:
                system = "base24"

        slug = data.get("slug")
        if slug is None:
            slug = slugify.slugify(scheme_file.stem, only_ascii=True)

        description = data.get("description", "")
        variant = data.get("variant", "unknown")

        return ColorScheme(
            name=data["name"],
            author=data["author"],
            system=system,
            slug=slug,
            description=description,
            variant=variant,
            palette=palette,
        )


def load_schemes(file_spec: str = "*") -> SchemeDB:
    config = Base24ViewerConfig()

    if "*" not in file_spec:
        fs = file_spec + "*"
    else:
        fs = file_spec

    if not fs.endswith(".yaml"):
        fs = fs + ".yaml"

    schemes = {}
    files = config.scheme_dir.glob(fs)
    for scheme_file in files:
        schemes[scheme_file.name] = load_scheme(scheme_file)

    return schemes
