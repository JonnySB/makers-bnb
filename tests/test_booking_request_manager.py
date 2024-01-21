from lib.booking_request_manager import BookingRequestManager
from datetime import date


# tests BookingRequestManager initialises with correct attrs
def test_initialises_with_given_attributes():
    booking_request_manager_1 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 1, 1
    )
    assert booking_request_manager_1.booking_request_id == 1
    assert booking_request_manager_1.booking_id == 1
    assert booking_request_manager_1.space_name == "Cosy Cottage"
    assert booking_request_manager_1.guest_id == 2
    assert booking_request_manager_1.guest_username == "user2"
    assert booking_request_manager_1.booking_date == date(2023, 12, 1)
    assert booking_request_manager_1.booking_message == "Please can I stay?"
    assert booking_request_manager_1.status == "Pending"
    assert booking_request_manager_1.host_id == 1


# tests two BookingRequestManager objects with the same data are found equal
def test_booking_eq():
    booking_request_manager_1 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 1, 1
    )
    booking_request_manager_2 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 1, 1
    )
    assert booking_request_manager_1 == booking_request_manager_2


# test the correct string representation is printed for the BookingRequestManager
# object
def test_booking_repr():
    booking_request_manager_1 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 1, 1
    )
    assert (
        str(booking_request_manager_1)
        == "BookingRequest: 1, 1, Cosy Cottage, 2, user2, 2023-12-01, Please can I stay?, Pending, 1"
    )


# test status is set to 'Pending' if passed 1
def test_set_status_to_pending():
    booking_request_manager_1 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 1, 1
    )
    booking_request_manager_1.convert_status_num_to_str_repr(1)
    assert booking_request_manager_1.status == "Pending"


# test status is set to 'Accepted' if passed 2
def test_set_status_to_accepted():
    booking_request_manager_1 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 2, 1
    )
    booking_request_manager_1.convert_status_num_to_str_repr(2)
    assert booking_request_manager_1.status == "Accepted"


# test status is set to 'Declined' if passed 3
def test_set_status_to_declined():
    booking_request_manager_1 = BookingRequestManager(
        1, 1, "Cosy Cottage", 2, "user2", date(2023, 12, 1), "Please can I stay?", 3, 1
    )
    booking_request_manager_1.convert_status_num_to_str_repr(3)
    assert booking_request_manager_1.status == "Declined"
