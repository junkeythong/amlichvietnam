from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as _dt
    from .core import LunarDate


SOLAR_HOLIDAYS = {
    (1, 1): "Tết Dương Lịch",
    (30, 4): "Ngày Giải Phóng Miền Nam",
    (1, 5): "Ngày Quốc Tế Lao Động",
    (2, 9): "Ngày Quốc Khánh",
}

LUNAR_HOLIDAYS = {
    (1, 1): "Tết Nguyên Đán",
    (2, 1): "Tết Nguyên Đán",
    (3, 1): "Tết Nguyên Đán",
    (15, 1): "Rằm Tháng Giêng",
    (10, 3): "Giỗ Tổ Hùng Vương",
    (15, 4): "Lễ Phật Đản",
    (5, 5): "Tết Đoan Ngọ",
    (15, 7): "Lễ Vu Lan",
    (15, 8): "Tết Trung Thu",
}


def get_holiday(solar: _dt.date, lunar: LunarDate) -> Optional[str]:
    """
    Get Vietnamese holiday for a given solar and lunar date.
    Returns the name of the holiday or None.
    """
    # Priority: Lunar Tet then Solar then other Lunar
    if not lunar.leap:
        if (lunar.month, lunar.day) == (1, 1):
            return LUNAR_HOLIDAYS[(1, 1)]
        if (lunar.month, lunar.day) == (1, 2):
            return LUNAR_HOLIDAYS[(2, 1)]
        if (lunar.month, lunar.day) == (1, 3):
            return LUNAR_HOLIDAYS[(3, 1)]

    # Solar holidays
    s_key = (solar.day, solar.month)
    if s_key in SOLAR_HOLIDAYS:
        return SOLAR_HOLIDAYS[s_key]

    # Other lunar holidays
    if not lunar.leap:
        l_key = (lunar.day, lunar.month)
        if l_key in LUNAR_HOLIDAYS:
            return LUNAR_HOLIDAYS[l_key]

    return None
