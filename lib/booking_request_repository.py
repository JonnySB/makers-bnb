from lib.booking_request import BookingRequest


class BookingRequestRepository:
    def __init__(self, db_connection):
        self._connection = db_connection

    def get_host_requests(self, host_id):
        rows = self._connection.execute(
            "select booking_requests.id, booking_id, guest_id, booking_message, status from booking_requests "
            "join bookings on booking_id=bookings.id "
            "join spaces on bookings.space_id=spaces.id "
            "join users on spaces.user_id=users.id "
            "where users.id = %s; ",
            [host_id],
        )
        booking_requests = []
        for row in rows:
            booking_requests.append(
                BookingRequest(
                    row["id"],
                    row["booking_id"],
                    row["guest_id"],
                    row["booking_message"],
                    row["status"],
                )
            )

        return booking_requests
