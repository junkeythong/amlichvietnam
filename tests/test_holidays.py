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
