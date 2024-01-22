from lib import booking_request_manager_repository
from lib.booking_request_manager import BookingRequestManager
from lib.booking_request_manager_repository import BookingRequestManagerRepository
from datetime import date


# tests that when called with a particular host_id, the associated booking
# requests are returned as BookingRequestManager objects.
def test_get_BRM_by_host_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestManagerRepository(db_connection)

    booking_requests = booking_request_repo.get_BRM_by_host_id(1)
    assert booking_requests == [
        BookingRequestManager(
            1,
            1,
            "Enchanted Retreat",
            1,
            "user1",
            date(2024, 5, 10),
            "Would be great to stay!",
            1,
            1,
        ),
        BookingRequestManager(
            2,
            2,
            "Enchanted Retreat",
            2,
            "user2",
            date(2024, 5, 11),
            "Would be fab to stay!",
            1,
            1,
        ),
    ]


# tests that when called with a particular booking_request_id, the associated booking
# requests manager object (BRM) is returned as a BookingRequestManager objects.
def test_get_BRM_by_booking_request_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestManagerRepository(db_connection)

    booking_requests = booking_request_repo.get_BRM_by_booking_request_id(1)
    assert booking_requests == BookingRequestManager(
        1,
        1,
        "Enchanted Retreat",
        1,
        "user1",
        date(2024, 5, 10),
        "Would be great to stay!",
        1,
        1,
    )


# tests that when called with a particular booking_id, all the associated
# booking_request_ids are returned in a list
def test_get_booking_request_ids_by_booking_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestManagerRepository(db_connection)

    booking_requests = booking_request_repo.get_booking_request_ids_by_booking_id(1)
    assert booking_requests == [1]


# tests that when called with a particular booking_request_id, the
# booking_request.status is updated to '2' (accepted) in the database
def test_set_booking_request_status_to_accepted(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestManagerRepository(db_connection)

    # assert status = pending
    booking_requests = booking_request_repo.get_BRM_by_booking_request_id(1)
    assert booking_requests == BookingRequestManager(
        1,
        1,
        "Enchanted Retreat",
        1,
        "user1",
        date(2024, 5, 10),
        "Would be great to stay!",
        1,
        1,
    )

    booking_request_repo.set_booking_request_status_to_accepted(1)

    # assert status = pending
    booking_requests = booking_request_repo.get_BRM_by_booking_request_id(1)
    assert booking_requests == BookingRequestManager(
        1,
        1,
        "Enchanted Retreat",
        1,
        "user1",
        date(2024, 5, 10),
        "Would be great to stay!",
        2,
        1,
    )


# tests that when called with a particular booking_request_id, the
# booking_request.status is updated to '3' (declined) in the database
def test_set_booking_request_status_to_(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestManagerRepository(db_connection)

    # assert status = pending
    booking_requests = booking_request_repo.get_BRM_by_booking_request_id(1)
    assert booking_requests == BookingRequestManager(
        1,
        1,
        "Enchanted Retreat",
        1,
        "user1",
        date(2024, 5, 10),
        "Would be great to stay!",
        1,
        1,
    )

    booking_request_repo.set_booking_request_status_to_declined(1)

    # assert status = pending
    booking_requests = booking_request_repo.get_BRM_by_booking_request_id(1)
    assert booking_requests == BookingRequestManager(
        1,
        1,
        "Enchanted Retreat",
        1,
        "user1",
        date(2024, 5, 10),
        "Would be great to stay!",
        3,
        1,
    )


# tests that when called with a particular guest_id, the associated booking
# requests are returned as BookingRequestManager objects.
def test_get_BRM_by_guest_id(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    booking_request_repo = BookingRequestManagerRepository(db_connection)

    booking_requests = booking_request_repo.get_BRM_by_guest_id(1)
    assert booking_requests == [
        BookingRequestManager(
            1,
            1,
            "Enchanted Retreat",
            1,
            "user1",
            date(2024, 5, 10),
            "Would be great to stay!",
            1,
            1,
        ),
    ]
