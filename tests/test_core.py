import datetime as dt
import pytest

from lunar_vn import (
    LunarDate,
    jd_from_date,
    jd_to_date,
    solar_to_lunar,
    lunar_to_solar,
)

TZ_VN = 7.0


def test_jdn_known_values():
    # JDN reference: Jan 1, 2000 = 2451545
    assert jd_from_date(1, 1, 2000) == 2451545

    # Gregorian transition checks (as used by HND algorithm)
    assert jd_from_date(4, 10, 1582) == 2299160
    assert jd_from_date(15, 10, 1582) == 2299161


def test_jdn_roundtrip_known_dates():
    samples = [
        (1, 1, 2000),
        (31, 12, 1999),
        (4, 10, 1582),
        (15, 10, 1582),
        (10, 2, 2024),
        (29, 1, 2025),
        (17, 2, 2026),
    ]
    for dd, mm, yy in samples:
        jdn = jd_from_date(dd, mm, yy)
        dd2, mm2, yy2 = jd_to_date(jdn)
        assert (dd2, mm2, yy2) == (dd, mm, yy)


@pytest.mark.parametrize(
    "solar, expected_lunar",
    [
        # Vietnamese New Year (Tet) dates
        ((10, 2, 2024), LunarDate(1, 1, 2024, False)),
        ((29, 1, 2025), LunarDate(1, 1, 2025, False)),
        ((17, 2, 2026), LunarDate(1, 1, 2026, False)),
    ],
)
def test_tet_solar_to_lunar(solar, expected_lunar):
    got = solar_to_lunar(solar, time_zone=TZ_VN)
    assert got == expected_lunar


@pytest.mark.parametrize(
    "lunar, expected_solar",
    [
        (LunarDate(1, 1, 2024, False), dt.date(2024, 2, 10)),
        (LunarDate(1, 1, 2025, False), dt.date(2025, 1, 29)),
        (LunarDate(1, 1, 2026, False), dt.date(2026, 2, 17)),
    ],
)
def test_tet_lunar_to_solar(lunar, expected_solar):
    got = lunar_to_solar(lunar, time_zone=TZ_VN)
    assert got == expected_solar


def test_leap_month_2004_start_day():
    # From HND calrules: leap month in 2004 is the month from 21/3/2004 to 18/4/2004,
    # so 21/3/2004 should be 1/2 leap (month 2 leap) in lunar year 2004.
    got = solar_to_lunar((21, 3, 2004), time_zone=TZ_VN)
    assert got == LunarDate(1, 2, 2004, True)

    # Reverse should map back
    back = lunar_to_solar(LunarDate(1, 2, 2004, True), time_zone=TZ_VN)
    assert back == dt.date(2004, 3, 21)


def test_invalid_leap_flag_raises():
    # 2004 leap month is month 2 (leap). Marking month 3 as leap should be invalid.
    with pytest.raises(ValueError):
        lunar_to_solar(LunarDate(1, 3, 2004, True), time_zone=TZ_VN)


def test_roundtrip_solar_lunar_solar_small_range():
    # Consistency test: solar -> lunar -> solar must return original date.
    # Keep it small to run fast but cover many months/years.
    start = dt.date(1990, 1, 1)
    end = dt.date(2030, 12, 31)

    step_days = 11  # sample every 11 days
    d = start
    while d <= end:
        lunar = solar_to_lunar(d, time_zone=TZ_VN)
        d2 = lunar_to_solar(lunar, time_zone=TZ_VN)
        assert d2 == d
        d += dt.timedelta(days=step_days)

