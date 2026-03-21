from __future__ import annotations

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]
CHI = [
    "Tý",
    "Sửu",
    "Dần",
    "Mão",
    "Thìn",
    "Tỵ",
    "Ngọ",
    "Mùi",
    "Thân",
    "Dậu",
    "Tuất",
    "Hợi",
]


def get_year_can_chi(year: int) -> str:
    """Get the Can Chi name of a year."""
    can_idx = (year + 6) % 10
    chi_idx = (year + 8) % 12
    return f"{CAN[can_idx]} {CHI[chi_idx]}"


def get_month_can_chi(year: int, month: int) -> str:
    """
    Get the Can Chi name of a lunar month.
    The first month of the year is always 'Dần' branch.
    'month' here is the lunar month (1 to 12).
    """
    year_can_idx = (year + 6) % 10
    # Formula for 1st month (Dần) Can: (year_can_idx * 2 + 2) % 10
    start_month_can_idx = (year_can_idx * 2 + 2) % 10

    # Lunar months are 1-indexed. Branch for month m: (m + 1) % 12
    # Branch 0: Tý, 1: Sửu, 2: Dần...
    # Month 1 is Dần (index 2).
    month_can_idx = (start_month_can_idx + month - 1) % 10
    month_chi_idx = (month + 1) % 12

    return f"{CAN[month_can_idx]} {CHI[month_chi_idx]}"


def get_day_can_chi(jdn: int) -> str:
    """Get the Can Chi name of a day from Julian Day Number."""
    can_idx = (jdn + 9) % 10
    chi_idx = (jdn + 1) % 12
    return f"{CAN[can_idx]} {CHI[chi_idx]}"


def get_hour_can_chi(day_jdn: int, hour: int) -> str:
    """
    Get the Can Chi name of a 2-hour period.
    'hour' is 0 to 23 (solar hour).
    """
    day_can_idx = (day_jdn + 9) % 10

    # Branch index: Tý is 0, Sửu is 1...
    # Hour 23-1 is Tý, 1-3 is Sửu...
    # Formula: ((hour + 1) // 2) % 12
    chi_idx = ((hour + 1) // 2) % 12

    # Hour Can: (day_can_idx * 2 + chi_idx) % 10
    # Wait, the rule is Tý hour Can depends on Day Can.
    # Day Can Giáp (0)/Kỷ (5) -> Tý hour is Giáp (0).
    # Since chi_idx for Tý is 0, (0 * 2 + 0) % 10 = 0. Correct.
    can_idx = (day_can_idx * 2 + chi_idx) % 10

    return f"{CAN[can_idx]} {CHI[chi_idx]}"
