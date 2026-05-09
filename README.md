# Âm Lịch Việt Nam - Vietnamese Lunar Calendar for Python 🇻🇳

[![PyPI version](https://img.shields.io/pypi/v/lunar-vn.svg)](https://pypi.org/project/lunar-vn/)
[![CI](https://github.com/junkeythong/amlichvietnam/actions/workflows/ci.yml/badge.svg)](https://github.com/junkeythong/amlichvietnam/actions/workflows/ci.yml)
[![License](https://img.shields.io/pypi/l/lunar-vn.svg)](https://pypi.org/project/lunar-vn/)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/lunar-vn?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=MAGENTA&left_text=downloads)](https://pypi.org/project/lunar-vn/)
[![Monthly Downloads](https://static.pepy.tech/personalized-badge/lunar-vn?period=month&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=BLUE&left_text=downloads/month)](https://pypi.org/project/lunar-vn/)

**Goal:** lightweight - typed - dependency-free - accurate - easy to trust

`lunar-vn` is designed for:

- Vietnamese calendar apps
- Tết and lunar holiday reminders
- HR, payroll, booking, and event systems
- Bots that need Vietnamese lunar dates
- Cultural, astrology, and Can Chi applications
- Backend services that need a small, typed, no-dependency package
- Personal and business systems that need predictable calendar behavior

---

## Features

- **No Dependencies**: Small package with strict typing support (PEP-561 compliant).
- **Production-friendly**: Deterministic local functions with no runtime service dependency.
- **Support Can Chi**: Heavenly Stems and Earthly Branches for year, month, day, hour.
- **Vietnamese Holidays**: Common solar and lunar holidays included.
- **Holiday Lists**: Get year-specific Vietnamese holiday dates for app and reminder workflows.
- **Convert Solar → Lunar**: Accepts robust `datetime.date` inputs.
- **Convert Lunar → Solar**: Accurate conversion using the Ho Ngoc Duc algorithm.
- **Supported Range**: Solar dates from **1900-01-01 to 2100-12-31**.
- **Leap month support**: Handled automatically.
- **Timezone support**: Default `UTC+7` (Vietnam).
- **Full-range tested**: The test suite roundtrips every supported solar date.
- **Processing Time Benchmark**: High-performance conversions using internal caching (`clear_cache` supported).

---

## Installation

```bash
pip install lunar-vn
```

---

## Usage Examples

### Basic Conversion
```python
import datetime as dt
from lunar_vn import solar_to_lunar, lunar_to_solar, LunarDate

# Vietnamese Lunar New Year 2026
solar_date = dt.date(2026, 2, 17)
lunar_date = solar_to_lunar(solar_date)

print(lunar_date) # LunarDate(day=1, month=1, year=2026, leap=False)

# Lunar -> Solar
print(lunar_to_solar(LunarDate(1, 1, 2026))) # 2026-02-17
```

### Get today's Vietnamese lunar date
```python
import datetime as dt
from lunar_vn import solar_to_lunar

today = dt.date.today()
lunar = solar_to_lunar(today)

print(f"Solar: {today}")
print(f"Lunar: {lunar.day}/{lunar.month}/{lunar.year}")
print(f"Leap month: {lunar.leap}")
```

### Can Chi and Holidays
```python
from lunar_vn import solar_to_lunar, can_chi, holidays, list_holidays
import datetime as dt

date = dt.date(2024, 2, 10)
lunar = solar_to_lunar(date)

# Get Year Can Chi
print(can_chi.get_year_can_chi(lunar.year))  # Giáp Thìn

# Get Day Can Chi (requires JDN)
from lunar_vn import jd_from_date
jdn = jd_from_date(date.day, date.month, date.year)
print(can_chi.get_day_can_chi(jdn))  # Giáp Thìn

# Check for Holiday
print(holidays.get_holiday(date))  # Tết Nguyên Đán

# List holidays observed in a Gregorian year
for solar_date, name in list_holidays(2026):
    print(solar_date, name)
```

---

## Vietnamese Holidays

`lunar-vn` includes common Vietnamese solar and lunar holidays.

Solar holidays include:

- Tết Dương Lịch
- Ngày Lễ Tình Nhân (Valentine)
- Ngày Quốc Tế Phụ Nữ
- Ngày Giải Phóng Miền Nam
- Ngày Quốc Tế Lao Động
- Ngày Quốc Tế Thiếu Nhi
- Ngày Quốc Khánh
- Ngày Phụ Nữ Việt Nam
- Ngày Nhà Giáo Việt Nam
- Ngày Thành Lập Quân Đội Nhân Dân Việt Nam
- Lễ Giáng Sinh

Lunar holidays include:

- Tết Nguyên Đán
- Rằm Tháng Giêng
- Tết Hàn Thực
- Giỗ Tổ Hùng Vương
- Lễ Phật Đản
- Tết Đoan Ngọ
- Lễ Thất Tịch
- Lễ Vu Lan
- Tết Trung Thu
- Tết Hạ Nguyên
- Tết Ông Công Ông Táo

Generic lunar reminders are also returned for non-leap months:

- Mùng 1
- Rằm

Specific lunar holidays still take precedence over these reminders.

---

## Benchmark

To run the benchmark script:
```bash
PYTHONPATH=src python3 scripts/benchmark.py
```
*Expected: > 100,000 conversions per second.*

When installed as a package, `python scripts/benchmark.py` also works.

---

## Accuracy and Scope

`lunar-vn` focuses on the core Vietnamese lunar calendar use case: conversion,
Can Chi naming, and common holiday lookup. It intentionally avoids broader
Vạn Sự, astrology, and auspicious-day features so the API stays small and easy
to verify.

The supported solar date range is **1900-01-01 through 2100-12-31**. The test
suite includes an exhaustive solar → lunar → solar roundtrip across that full
range.

---

## Comparison with Chinese Lunar Calendar

See [documentation](docs/comparison_chinese_lunar.md).

---

## Attribution

The Vietnamese lunar calendar algorithm is described by **Ho Ngoc Duc** on:
[https://xemamlich.uhm.vn](https://xemamlich.uhm.vn)

This library is a Python re-implementation of the published algorithm.

---

## License

MIT License.
