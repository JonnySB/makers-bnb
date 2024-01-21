from lib.booking_request import BookingRequest
from lib.booking_request_repository import BookingRequestRepository


def test_get_host_requests(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestRepository(db_connection)

    booking_requests = booking_request_repo.get_by_host_id(1)
    assert booking_requests == [
        BookingRequest(1, 1, 1, "Would be great to stay!", 1),
        BookingRequest(2, 1, 2, "Would be fab to stay!", 1),
        BookingRequest(3, 1, 3, "Would be awesome to stay!", 1),
    ]
