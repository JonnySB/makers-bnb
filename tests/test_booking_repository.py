from lib.booking_repository import BookingRepository
from lib.booking import Booking
from datetime import date


# test get bookings by space_id
def test_get_booking_by_space_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_repository = BookingRepository(db_connection)

    rows = booking_repository.get_bookings_by_space_id(1)

    assert rows == [
        Booking(1, date(2024, 5, 10), False, 1),
        Booking(2, date(2024, 5, 11), False, 1),
        Booking(3, date(2024, 5, 12), True, 1),
    ]


def test_updated_booking_availability_to_false(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_repository = BookingRepository(db_connection)

    rows = booking_repository.get_bookings_by_space_id(1)

    # ensure Booking (id=1) availability is set to True
    assert rows == [
        Booking(1, date(2024, 5, 10), False, 1),
        Booking(2, date(2024, 5, 11), False, 1),
        Booking(3, date(2024, 5, 12), True, 1),
    ]

    # set Booking (id=1) availability to True
    booking_repository.set_booking_availability_to_false(3)

    # assert booking (id=1) availability has been updated
    rows = booking_repository.get_bookings_by_space_id(1)
    assert rows == [
        Booking(1, date(2024, 5, 10), False, 1),
        Booking(2, date(2024, 5, 11), False, 1),
        Booking(3, date(2024, 5, 12), False, 1),
    ]


def test_updated_booking_availability_to_true(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_repository = BookingRepository(db_connection)

    rows = booking_repository.get_bookings_by_space_id(1)

    # ensure Booking (id=1) availability is set to True
    assert rows == [
        Booking(1, date(2024, 5, 10), False, 1),
        Booking(2, date(2024, 5, 11), False, 1),
        Booking(3, date(2024, 5, 12), True, 1),
    ]

    # set Booking (id=1) availability to True
    booking_repository.set_booking_availability_to_true(1)

    # assert booking (id=1) availability has been updated
    rows = booking_repository.get_bookings_by_space_id(1)
    assert rows == [
        Booking(1, date(2024, 5, 10), True, 1),
        Booking(2, date(2024, 5, 11), False, 1),
        Booking(3, date(2024, 5, 12), True, 1),
    ]


# test that when called, a database record is created and a Booking id with an
# updated booking id is returned
def test_add_booking_to_db(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)

    booking = Booking(None, date(2024, 5, 13), True, 1)
    repository.add_booking_to_db(booking)

    bookings = repository.get_bookings_by_space_id(1)
    assert bookings == [
        Booking(1, date(2024, 5, 10), False, 1),
        Booking(2, date(2024, 5, 11), False, 1),
        Booking(3, date(2024, 5, 12), True, 1),
        Booking(13, date(2024, 5, 13), True, 1),
    ]


# tests that when called with a booking id, a corresponding Booking object is
# returned
def test_get_booking_by_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)

    booking = repository.get_booking_by_id(1)
    assert booking == Booking(1, date(2024, 5, 10), False, 1)
