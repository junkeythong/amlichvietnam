import pytest
from lunar_vn import can_chi, jd_from_date, solar_to_lunar

def test_year_can_chi():
    assert can_chi.get_year_can_chi(2024) == "Giáp Thìn"
    assert can_chi.get_year_can_chi(2025) == "Ất Tỵ"
    assert can_chi.get_year_can_chi(2026) == "Bính Ngọ"

def test_month_can_chi():
    # 2024 is Giáp Thìn. Month 1 (Dần) should be Bính Dần.
    assert can_chi.get_month_can_chi(2024, 1) == "Bính Dần"
    assert can_chi.get_month_can_chi(2024, 2) == "Đinh Mão"

def test_day_can_chi():
    # 2024-03-21 (Solar) is 2024-02-12 (Lunar).
    # JD for 2024-03-21 is 2460391.
    jdn = jd_from_date(21, 3, 2024)
    assert can_chi.get_day_can_chi(jdn) == "Giáp Thân"

def test_hour_can_chi():
    # Day 2024-03-21 is Giáp Tuất (Can Giáp index 0).
    # Hour 12:00 (solar) is Ngọ branch (index 6).
    # Can index = (0 * 2 + 6) % 10 = 6 (Canh).
    # So 12:00 is Canh Ngọ.
    jdn = jd_from_date(21, 3, 2024)
    assert can_chi.get_hour_can_chi(jdn, 12) == "Canh Ngọ"
    # Hour 00:00 is Tý. Can index = (0 * 2 + 0) % 10 = 0 (Giáp).
    assert can_chi.get_hour_can_chi(jdn, 0) == "Giáp Tý"
