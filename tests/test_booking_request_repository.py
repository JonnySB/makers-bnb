from lib.booking_request import BookingRequest
from lib.booking_request_repository import BookingRequestRepository


# tests that when called with a particular host_id, the associated booking
# requests are returned as BookingRequest objects.
def test_get_booking_request_by_host_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestRepository(db_connection)

    booking_requests = booking_request_repo.get_booking_requests_by_host_id(1)
    assert booking_requests == [
        BookingRequest(1, 1, 1, "Would be great to stay!", 1),
        BookingRequest(2, 2, 2, "Would be fab to stay!", 1),
    ]


# tests that when called with a BookingRequests object, an associated record is
# created in the booking_requests table of the database
def test_add_booking_request_to_db(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestRepository(db_connection)

    booking_request = BookingRequest(3, 1, 3, "Would be awesome to stay!", 1)
    booking_request_repo.add_booking_request_to_db(booking_request)

    booking_requests = booking_request_repo.get_booking_requests_by_host_id(1)
    assert booking_requests == [
        BookingRequest(1, 1, 1, "Would be great to stay!", 1),
        BookingRequest(2, 2, 2, "Would be fab to stay!", 1),
        BookingRequest(4, 1, 3, "Would be awesome to stay!", 1),
    ]
