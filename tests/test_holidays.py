import datetime as dt
from lunar_vn import holidays, solar_to_lunar, LunarDate

def test_holidays():
    # Tet 2024
    date = dt.date(2024, 2, 10)
    assert holidays.get_holiday(date) == "Tết Nguyên Đán"
    
    # Solar Holiday: Apr 30
    date_solar = dt.date(2024, 4, 30)
    assert holidays.get_holiday(date_solar) == "Ngày Giải Phóng Miền Nam"
    
    # Hung Kings: 10/3 Lunar
    # In 2024, 10/3 Lunar is 2024-04-18 Solar
    date_hung = dt.date(2024, 4, 18)
    assert holidays.get_holiday(date_hung) == "Giỗ Tổ Hùng Vương"

def test_no_holiday():
    date = dt.date(2024, 3, 21)
    assert holidays.get_holiday(date) is None

def test_all_lunar_holidays():
    # Mocking solar date is enough since we provide lunar mapping directly
    mapping = {
        LunarDate(1, 1, 2024): "Tết Nguyên Đán",
        LunarDate(2, 1, 2024): "Tết Nguyên Đán",
        LunarDate(3, 1, 2024): "Tết Nguyên Đán",
        LunarDate(15, 1, 2024): "Rằm Tháng Giêng",
        LunarDate(10, 3, 2024): "Giỗ Tổ Hùng Vương",
        LunarDate(15, 4, 2024): "Lễ Phật Đản",
        LunarDate(5, 5, 2024): "Tết Đoan Ngọ",
        LunarDate(15, 7, 2024): "Lễ Vu Lan",
        LunarDate(15, 8, 2024): "Tết Trung Thu",
    }
    dummy = dt.date(2024, 1, 2)
    for l_date, name in mapping.items():
        assert holidays.get_holiday(dummy, lunar=l_date) == name
        
    # Leap month should not duplicate holidays
    leap_lunar = LunarDate(15, 8, 2024, leap=True)
    assert holidays.get_holiday(dummy, lunar=leap_lunar) is None

def test_solar_holidays_full():
    mapping = {
        dt.date(2024, 1, 1): "Tết Dương Lịch",
        dt.date(2024, 4, 30): "Ngày Giải Phóng Miền Nam",
        dt.date(2024, 5, 1): "Ngày Quốc Tế Lao Động",
        dt.date(2024, 9, 2): "Ngày Quốc Khánh",
    }
    for s_date, name in mapping.items():
        assert holidays.get_holiday(s_date) == name
