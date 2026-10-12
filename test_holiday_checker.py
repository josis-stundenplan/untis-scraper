import datetime
from holiday_checker import is_school_holiday

def test_known_holidays_2025():
    # 03.02.2025 ist Halbjahresferien in Niedersachsen
    is_holiday, name = is_school_holiday(datetime.date(2025, 2, 3))
    assert is_holiday is True
    assert name is not None
    assert "Ferien" in name or "Halbjahresferien" in name

    # 15.07.2025 ist Sommerferien in Niedersachsen
    is_holiday_sommer, name_sommer = is_school_holiday(datetime.date(2025, 7, 15))
    assert is_holiday_sommer is True
    assert "Sommerferien" in name_sommer

def test_regular_school_days():
    # 14.02.2025 ist ein regulärer Schultag
    is_holiday, name = is_school_holiday(datetime.date(2025, 2, 14))
    assert is_holiday is False
    assert name is None

def test_cross_year_christmas_holiday():
    # 02.01.2025 ist Weihnachtsferien
    is_holiday, name = is_school_holiday(datetime.date(2025, 1, 2))
    assert is_holiday is True
    assert "Weihnachtsferien" in name
