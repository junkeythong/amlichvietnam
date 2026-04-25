from .core import (
    LunarDate,
    jd_from_date,
    jd_to_date,
    convert_solar_to_lunar,
    convert_lunar_to_solar,
    solar_to_lunar,
    lunar_to_solar,
    clear_cache,
    SUPPORTED_YEAR_RANGE,
)
from . import can_chi
from . import holidays

from importlib.metadata import version, PackageNotFoundError
try:
    __version__ = version("lunar_vn")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "LunarDate",
    "jd_from_date",
    "jd_to_date",
    "convert_solar_to_lunar",
    "convert_lunar_to_solar",
    "solar_to_lunar",
    "lunar_to_solar",
    "clear_cache",
    "SUPPORTED_YEAR_RANGE",
    "can_chi",
    "holidays",
]

