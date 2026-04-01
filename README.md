# Âm Lịch Việt Nam

[![PyPI version](https://img.shields.io/pypi/v/lunar-vn.svg)](https://pypi.org/project/lunar-vn/)
[![CI](https://github.com/junkeythong/amlichvietnam/actions/workflows/ci.yml/badge.svg)](https://github.com/junkeythong/amlichvietnam/actions/workflows/ci.yml)
[![PyPI Downloads](https://static.pepy.tech/personalized-badge/lunar-vn?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=MAGENTA&left_text=downloads)](https://pypi.org/project/lunar-vn/)

Python library for converting between **Gregorian (solar) calendar** and **Vietnamese lunar calendar**.

**Goal:** lightweight - simple – accurate – easy to reuse - **Enterprise Ready**

---

## FEATURES

- **No Dependencies**: Ready for enterprise usage.
- **Support Can Chi**: Heavenly Stems and Earthly Branches for year, month, day, hour.
- **Vietnamese Holidays**: Common solar and lunar holidays included.
- **Convert Solar → Lunar**: (`dd/mm/yyyy → lunar day/month/year with leap month flag`)
- **Convert Lunar → Solar**: Accurate conversion using the Ho Ngoc Duc algorithm.
- **Leap month support**: Handled automatically.
- **Timezone support**: Default `UTC+7` (Vietnam).
- **Processing Time Benchmark**: High-performance conversions.P

---

## INSTALLATION

```bash
pip install lunar-vn
```

---

## USAGE EXAMPLE

### Basic Conversion
```python
import datetime as dt
from lunar_vn import solar_to_lunar, lunar_to_solar, LunarDate

# Solar -> Lunar
l = solar_to_lunar((17, 2, 2026))   # Vietnamese Lunar New Year 2026
print(l)  # LunarDate(day=1, month=1, year=2026, leap=False)

# Lunar -> Solar
d = lunar_to_solar(LunarDate(1, 1, 2026))
print(d)  # 2026-02-17
```

### Can Chi and Holidays
```python
from lunar_vn import solar_to_lunar, can_chi, holidays
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
```

---

## BENCHMARK

To run the benchmark script:
```bash
python scripts/benchmark.py
```
*Expected: > 100,000 conversions per second.*

---

## COMPARISON WITH CHINESE LUNAR CALENDAR

See [documentation](docs/comparison_chinese_lunar.md).

---

## ATTRIBUTION

The Vietnamese lunar calendar algorithm is described by **Ho Ngoc Duc**
on the website: https://xemamlich.uhm.vn

This library is a Python re-implementation of the published algorithm.

---

## LICENSE

MIT License
