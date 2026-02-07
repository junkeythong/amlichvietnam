Am Lich Viet Nam

Python library for converting between Gregorian (solar) calendar
and Vietnamese lunar calendar.

Goal: simple – accurate – easy to reuse


FEATURES

- Convert Solar -> Lunar (dd/mm/yyyy -> lunar day/month/year with leap month flag)
- Convert Lunar -> Solar
- Leap month support
- Timezone support (parameter: time_zone, default UTC+7 – Vietnam)


INSTALLATION

#TODO Install via pip (after publishing):
pip install amlichvietnam


LOCAL TESTING

pip install -e .
pip install pytest
pytest -q


USAGE EXAMPLE

import datetime as dt
from lunar_vn import solar_to_lunar, lunar_to_solar, LunarDate

# Solar -> Lunar
l = solar_to_lunar((17, 2, 2026))   # Vietnamese Lunar New Year 2026
print(l) # LunarDate(day=1, month=1, year=2026, leap=False)

# Lunar -> Solar
d = lunar_to_solar(LunarDate(1, 1, 2026))
print(d) # 2026-02-17

# Using datetime.date
l2 = solar_to_lunar(dt.date(2024, 2, 10))
print(l2) # LunarDate(day=1, month=1, year=2024, leap=False)


ATTRIBUTION

The Vietnamese lunar calendar algorithm is described by Ho Ngoc Duc
on the website: https://xemamlich.uhm.vn

This library is a Python re-implementation of the published algorithm.
No original source code is copied.


LICENSE

MIT License

