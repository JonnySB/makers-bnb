from lib.booking_request import BookingRequest
from datetime import date

"""
Initialises with given attributes
"""


def test_initialises_with_given_attributes():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    assert date1.booking_id == 1
    assert date1.guest_id == 1
    assert date1.booking_message == "Please may I book!"
    assert date1.status == "pending"


def test_update_status():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    date1.set_status(2)
    assert date1.status == "accepted"


def test_booking_eq():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    date2 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    assert date1 == date2


def test_booking_repr():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    assert str(date1) == "BookingRequest: 1, 1, 1, Please may I book!, pending"
