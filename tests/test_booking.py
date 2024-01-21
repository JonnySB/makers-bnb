from lib.booking import Booking
from datetime import date


# tests Booking initialises with correct attrs
def test_initialises_with_given_attributes():
    date1 = Booking(1, date(2023, 12, 5), True, 1)
    assert date1.id == 1
    assert date1.date == date(2023, 12, 5)
    assert date1.is_available == True
    assert date1.space_id == 1


# tests two Booking objects with the same data are found equal
def test_booking_eq():
    date1 = Booking(1, date(2023, 12, 5), True, 1)
    date2 = Booking(1, date(2023, 12, 5), True, 1)
    assert date1 == date2


# test the correct string representation is printed for the Booking object
def test_booking_repr():
    date1 = Booking(1, date(2023, 12, 5), True, 1)
    assert str(date1) == "Booking(1, 2023-12-05, True, 1)"
