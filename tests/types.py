from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class File:
    """Validator for a generated file."""
    must_have_content: bool = True
    contains: Optional[list[str]] = None
    is_binary: bool = False