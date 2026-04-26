from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import datetime as _dt
    from .core import LunarDate


SOLAR_HOLIDAYS = {
    (1, 1): "Tết Dương Lịch",
    (14, 2): "Ngày Lễ Tình Nhân",
    (8, 3): "Ngày Quốc Tế Phụ Nữ",
    (30, 4): "Ngày Giải Phóng Miền Nam",
    (1, 5): "Ngày Quốc Tế Lao Động",
    (1, 6): "Ngày Quốc Tế Thiếu Nhi",
    (2, 9): "Ngày Quốc Khánh",
    (20, 10): "Ngày Phụ Nữ Việt Nam",
    (20, 11): "Ngày Nhà Giáo Việt Nam",
    (22, 12): "Ngày Thành Lập Quân Đội Nhân Dân Việt Nam",
    (25, 12): "Lễ Giáng Sinh",
}

LUNAR_HOLIDAYS = {
    (1, 1): "Tết Nguyên Đán",
    (2, 1): "Tết Nguyên Đán",
    (3, 1): "Tết Nguyên Đán",
    (15, 1): "Rằm Tháng Giêng",
    (3, 3): "Tết Hàn Thực",
    (10, 3): "Giỗ Tổ Hùng Vương",
    (15, 4): "Lễ Phật Đản",
    (5, 5): "Tết Đoan Ngọ",
    (7, 7): "Lễ Thất Tịch",
    (15, 7): "Lễ Vu Lan",
    (15, 8): "Tết Trung Thu",
    (15, 10): "Tết Hạ Nguyên",
    (23, 12): "Tết Ông Công Ông Táo",
}


def get_holiday(solar: _dt.date, lunar: Optional[LunarDate] = None) -> Optional[str]:
    """
    Get Vietnamese holiday for a given solar date.
    Calculates lunar date automatically if not provided.
    """
    from .core import solar_to_lunar
    
    if lunar is None:
        lunar = solar_to_lunar(solar)

    # Priority: Lunar Tet then Solar then other Lunar
    if not lunar.leap:
        if (lunar.day, lunar.month) == (1, 1):
            return LUNAR_HOLIDAYS[(1, 1)]
        if (lunar.day, lunar.month) == (2, 1):
            return LUNAR_HOLIDAYS[(2, 1)]
        if (lunar.day, lunar.month) == (3, 1):
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
