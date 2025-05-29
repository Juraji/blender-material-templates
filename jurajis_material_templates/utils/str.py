import re


def strip_suffix(name: str) -> str:
    """Remove Blender’s .001/.002… suffixes."""
    return re.sub(r"\.\d{3}$", "", name)
