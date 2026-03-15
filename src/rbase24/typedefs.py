from typing import TypedDict, NotRequired
from enum import StrEnum

Color = str


class Palette(TypedDict):
    base00: Color
    base01: Color
    base02: Color
    base03: Color
    base04: Color
    base05: Color
    base06: Color
    base07: Color
    base08: Color
    base09: Color
    base0A: Color
    base0B: Color
    base0C: Color
    base0D: Color
    base0E: Color
    base0F: Color
    base10: NotRequired[Color]
    base11: NotRequired[Color]
    base12: NotRequired[Color]
    base13: NotRequired[Color]
    base14: NotRequired[Color]
    base15: NotRequired[Color]
    base16: NotRequired[Color]
    base17: NotRequired[Color]


class SchemeKeys(StrEnum):
    FILE = "file"
    SCHEME = "scheme"
    AUTHOR = "author"
    SYSTEM = "system"
    SLUG = "slug"
    DESCRIPTION = "description"
    VARIANT = "variant"


class ColorScheme(TypedDict):
    file: str
    scheme: str
    author: str
    system: str
    slug: str
    description: str
    variant: str
    palette: Palette


SchemeDB = dict[str, ColorScheme]
