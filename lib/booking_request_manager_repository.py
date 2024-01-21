from lib.booking_request_manager import BookingRequestManager


class BookingRequestManagerRepository:
    def __init__(self, db_connection):
        self._connection = db_connection

    # Call with host_id to get back all Booking Request Manager objects
    # associated with ID.
    def get_BRM_by_host_id(self, host_id: int) -> list[BookingRequestManager]:
        rows = self._connection.execute(
            """
            SELECT
                booking_requests.id as booking_request_id,
                booking_id,
                bookings.date as booking_date,
                spaces.name as space_name,
                guests.id as guest_id,
                guests.username as guest_username,
                booking_message,
                status,
                hosts.id as host_id
            FROM booking_requests
            JOIN bookings on booking_id=bookings.id
            JOIN spaces on bookings.space_id=spaces.id
            JOIN users guests on guest_id = guests.id
            JOIN users hosts on spaces.user_id = hosts.id
            WHERE hosts.id = %s
            ORDER BY status;
            """,
            [host_id],
        )
        booking_requests = []
        for row in rows:
            booking_requests.append(
                BookingRequestManager(
                    row["booking_request_id"],
                    row["booking_id"],
                    row["space_name"],
                    row["guest_id"],
                    row["guest_username"],
                    row["booking_date"],
                    row["booking_message"],
                    row["status"],
                    row["host_id"],
                )
            )

        return booking_requests

    # When called with booking_request_id, collects all relevent details from
    # tables storing Booking Request Manager (BMR) information and constructs
    # BookingRequestManager object
    def get_BRM_by_booking_request_id(
        self, booking_request_id: int
    ) -> BookingRequestManager:
        rows = self._connection.execute(
            """
            SELECT
                booking_requests.id as booking_request_id,
                booking_id,
                bookings.date as booking_date,
                spaces.name as space_name,
                guests.id as guest_id,
                guests.username as guest_username,
                booking_message,
                status,
                hosts.id as host_id
            FROM booking_requests
            JOIN bookings on booking_id=bookings.id
            JOIN spaces on bookings.space_id=spaces.id
            JOIN users guests on guest_id = guests.id
            JOIN users hosts on spaces.user_id = hosts.id
            WHERE booking_requests.id = %s;
            """,
            [booking_request_id],
        )
        row = rows[0]
        return BookingRequestManager(
            row["booking_request_id"],
            row["booking_id"],
            row["space_name"],
            row["guest_id"],
            row["guest_username"],
            row["booking_date"],
            row["booking_message"],
            row["status"],
            row["host_id"],
        )

    # When called with booking_id, returns a list of all associated booking
    # request ids. I.e. to return requests against a specific date.
    def get_booking_request_ids_by_booking_id(self, booking_id: int) -> list[int]:
        rows = self._connection.execute(
            """
            SELECT id FROM booking_requests
            WHERE booking_id = %s
            """,
            [booking_id],
        )
        booking_request_ids = []
        for row in rows:
            booking_request_ids.append(row["id"])

        return booking_request_ids

    # When called with a specific booking_request_id, set status to 2, which is
    # converted to 'Accepted' when a BookingRequestManager object is created
    def set_booking_request_status_to_accepted(self, booking_request_id: int):
        self._connection.execute(
            """
            UPDATE booking_requests
            SET status = 2
            WHERE id = %s;
            """,
            [booking_request_id],
        )

    # When called with a specific booking_request_id, set status to 3, which is
    # converted to 'Declined' when a BookingRequestManager object is created
    def set_booking_request_status_to_declined(self, booking_request_id: int):
        self._connection.execute(
            """
            UPDATE booking_requests
            SET status = 3
            WHERE id = %s;
            """,
            [booking_request_id],
        )
