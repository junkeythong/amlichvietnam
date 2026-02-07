from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import datetime as _dt
import math
from typing import Tuple, Union

PI = math.pi


def _int_floor(x: float) -> int:
    """
    Equivalent to Hồ Ngọc Đức's INT(x) in the JS article:
    greatest integer not exceeding x (floor), including negatives.
    """
    return math.floor(x)


def jd_from_date(dd: int, mm: int, yy: int) -> int:
    """
    Convert Gregorian/Julian date to Julian day number (JDN).
    Uses Gregorian calendar after 5/10/1582 (JDN > 2299160) per the article.
    """
    a = _int_floor((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3

    jd = (
        dd
        + _int_floor((153 * m + 2) / 5)
        + 365 * y
        + _int_floor(y / 4)
        - _int_floor(y / 100)
        + _int_floor(y / 400)
        - 32045
    )

    if jd < 2299161:
        jd = dd + _int_floor((153 * m + 2) / 5) + 365 * y + _int_floor(y / 4) - 32083

    return int(jd)


def jd_to_date(jd: int) -> Tuple[int, int, int]:
    """
    Convert JDN to (day, month, year).
    """
    if jd > 2299160:  # After 5/10/1582, Gregorian calendar
        a = jd + 32044
        b = _int_floor((4 * a + 3) / 146097)
        c = a - _int_floor((b * 146097) / 4)
    else:  # Julian calendar
        b = 0
        c = jd + 32082

    d = _int_floor((4 * c + 3) / 1461)
    e = c - _int_floor((1461 * d) / 4)
    m = _int_floor((5 * e + 2) / 153)

    day = e - _int_floor((153 * m + 2) / 5) + 1
    month = m + 3 - 12 * _int_floor(m / 10)
    year = b * 100 + d - 4800 + _int_floor(m / 10)

    return int(day), int(month), int(year)


@lru_cache(maxsize=None)
def get_new_moon_day(k: int, time_zone: float) -> int:
    """
    Compute the day (JDN) of the k-th new moon since 1/1/1900.
    Ported from HND's JS in calrules.
    """
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = PI / 180

    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)

    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3

    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
    C1 = C1 + 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))

    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2

    JdNew = Jd1 + C1 - deltat
    return _int_floor(JdNew + 0.5 + time_zone / 24)


@lru_cache(maxsize=None)
def get_sun_longitude(jdn: int, time_zone: float) -> int:
    """
    Sun longitude sector (0..11) at local midnight of given JDN.
    Ported from HND's JS in calrules.
    """
    T = (jdn - 2451545.5 - time_zone / 24) / 36525
    T2 = T * T
    dr = PI / 180

    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2

    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)

    L = (L0 + DL) * dr
    L = L - PI * 2 * _int_floor(L / (PI * 2))  # normalize to (0, 2*pi)
    return _int_floor(L / PI * 6)


@lru_cache(maxsize=None)
def get_lunar_month11(yy: int, time_zone: float) -> int:
    """
    Find the JDN of the start day of lunar month 11 for solar year yy.
    """
    off = jd_from_date(31, 12, yy) - 2415021
    k = _int_floor(off / 29.530588853)
    nm = get_new_moon_day(k, time_zone)
    sun_long = get_sun_longitude(nm, time_zone)

    if sun_long >= 9:
        nm = get_new_moon_day(k - 1, time_zone)

    return nm


@lru_cache(maxsize=None)
def get_leap_month_offset(a11: int, time_zone: float) -> int:
    """
    Determine leap month position after month 11 starting at a11 (JDN).
    """
    k = _int_floor((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1  # start with month after lunar month 11
    last = 0
    arc = get_sun_longitude(get_new_moon_day(k + i, time_zone), time_zone)

    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, time_zone), time_zone)
        if arc == last or i >= 14:
            break

    return i - 1


@dataclass(frozen=True)
class LunarDate:
    day: int
    month: int
    year: int
    leap: bool = False  # True if leap month


def convert_solar_to_lunar(dd: int, mm: int, yy: int, time_zone: float = 7.0) -> LunarDate:
    """
    Convert solar date dd/mm/yy to lunar date using HND algorithm.
    time_zone = local time zone offset from UTC (Vietnam official: 7.0).
    """
    day_number = jd_from_date(dd, mm, yy)
    k = _int_floor((day_number - 2415021.076998695) / 29.530588853)

    month_start = get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = get_new_moon_day(k, time_zone)

    a11 = get_lunar_month11(yy, time_zone)
    b11 = a11

    if a11 >= month_start:
        lunar_year = yy
        a11 = get_lunar_month11(yy - 1, time_zone)
    else:
        lunar_year = yy + 1
        b11 = get_lunar_month11(yy + 1, time_zone)

    lunar_day = day_number - month_start + 1
    diff = _int_floor((month_start - a11) / 29)

    lunar_leap = 0
    lunar_month = diff + 11

    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = 1

    if lunar_month > 12:
        lunar_month -= 12

    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1

    return LunarDate(int(lunar_day), int(lunar_month), int(lunar_year), bool(lunar_leap))


def convert_lunar_to_solar(
    lunar_day: int,
    lunar_month: int,
    lunar_year: int,
    lunar_leap: int = 0,
    time_zone: float = 7.0,
) -> _dt.date:
    """
    Convert lunar date to solar date using HND algorithm.
    lunar_leap: 1 if leap month else 0 (same as HND JS).
    Raises ValueError if leap flag is inconsistent (like JS returns [0,0,0]).
    """
    if lunar_month < 11:
        a11 = get_lunar_month11(lunar_year - 1, time_zone)
        b11 = get_lunar_month11(lunar_year, time_zone)
    else:
        a11 = get_lunar_month11(lunar_year, time_zone)
        b11 = get_lunar_month11(lunar_year + 1, time_zone)

    off = lunar_month - 11
    if off < 0:
        off += 12

    if b11 - a11 > 365:
        leap_off = get_leap_month_offset(a11, time_zone)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12

        if lunar_leap != 0 and lunar_month != leap_month:
            raise ValueError("Invalid lunar leap flag for given lunar month/year")

        if lunar_leap != 0 or off >= leap_off:
            off += 1

    k = _int_floor(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + off, time_zone)
    dd, mm, yy = jd_to_date(month_start + lunar_day - 1)
    return _dt.date(yy, mm, dd)


# Convenience API
DateLike = Union[_dt.date, Tuple[int, int, int]]


def solar_to_lunar(date: DateLike, time_zone: float = 7.0) -> LunarDate:
    if isinstance(date, tuple):
        dd, mm, yy = date
        return convert_solar_to_lunar(dd, mm, yy, time_zone=time_zone)
    return convert_solar_to_lunar(date.day, date.month, date.year, time_zone=time_zone)


def lunar_to_solar(lunar: LunarDate, time_zone: float = 7.0) -> _dt.date:
    return convert_lunar_to_solar(
        lunar_day=lunar.day,
        lunar_month=lunar.month,
        lunar_year=lunar.year,
        lunar_leap=1 if lunar.leap else 0,
        time_zone=time_zone,
    )

