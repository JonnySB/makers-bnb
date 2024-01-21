from lib.booking_request import BookingRequest


class BookingRequestRepository:
    def __init__(self, db_connection):
        self._connection = db_connection

    # UNTESTED
    # when called with a booking_request_id, the corresponding data is fetched
    # from the database and a booking_request_object_is_returned
    def get_booking_request_by_id(self, id: int) -> BookingRequest:
        rows = self._connection.execute(
            """
            SELECT booking_requests.id,
                booking_id,
                guest_id,
                booking_message,
                status
            FROM booking_requests 
            JOIN bookings on booking_id=bookings.id 
            JOIN spaces on bookings.space_id=spaces.id 
            JOIN users on spaces.user_id=users.id 
            WHERE booking_requests.id = %s;
            """,
            [id],
        )
        row = rows[0]
        return BookingRequest(
            row["id"],
            row["booking_id"],
            row["guest_id"],
            row["booking_message"],
            row["status"],
        )

    # when called with a specific host id, return all associated booking
    # requests (as BookingRequest objects)
    def get_booking_requests_by_host_id(self, host_id: int) -> list[BookingRequest]:
        rows = self._connection.execute(
            """
            SELECT booking_requests.id,
                booking_id,
                guest_id,
                booking_message,
                status
            FROM booking_requests 
            JOIN bookings on booking_id=bookings.id 
            JOIN spaces on bookings.space_id=spaces.id 
            JOIN users on spaces.user_id=users.id 
            WHERE users.id = %s;
            """,
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

    # Insert booking request into booking_requests table of database
    def add_booking_request_to_db(self, booking_request: BookingRequest):
        self._connection.execute(
            """
            INSERT INTO booking_requests
            (booking_id, guest_id, booking_message, status)
            VALUES (%s, %s, %s, %s);
            """,
            [
                booking_request.booking_id,
                booking_request.guest_id,
                booking_request.booking_message,
                1,
            ],
        )

    # UNTESTED
    def delete_booking_request_by_booking_request_id(self, id):
        self._connection.execute(
            """
            DELETE FROM booking_requests
            WHERE id = %s;
            """,
            [id],
        )
