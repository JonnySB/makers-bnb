from lib.booking_request import BookingRequest
from datetime import date


# tests BookingRequest initialises with correct attrs
def test_initialises_with_given_attributes():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    assert date1.booking_id == 1
    assert date1.guest_id == 1
    assert date1.booking_message == "Please may I book!"
    assert date1.status == "Pending"


# tests two BookingRequest objects with the same data are found equal
def test_booking_eq():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    date2 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    assert date1 == date2


# test the correct string representation is printed for the BookingRequest
# object
def test_booking_repr():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    assert str(date1) == "BookingRequest: 1, 1, 1, Please may I book!, Pending"


# test status is set to 'Pending' if passed 1
def test_set_status_to_pending():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    date1.set_status(1)
    assert date1.status == "Pending"


# test status is set to 'Accepted' if passed 2
def test_set_status_to_accepted():
    date1 = BookingRequest(1, 1, 1, "Please may I book!", 1)
    date1.set_status(2)
    assert date1.status == "Accepted"


# test status is set to 'Declined' if passed 3
def test_set_status_to_declined():
    date1 = BookingRequest(1, 1, 1, "Declined", 1)
    date1.set_status(3)
    assert date1.status == "Declined"
