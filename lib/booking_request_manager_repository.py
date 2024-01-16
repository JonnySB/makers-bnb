from lib.booking_request_manager import BookingRequestManager


class BookingRequestManagerRepository:
    def __init__(self, db_connection):
        self._connection = db_connection

    def get_by_host_id(self, host_id):
        rows = self._connection.execute(
            """
            select
                booking_requests.id as booking_request_id,
                booking_id,
                bookings.date as booking_date,
                spaces.name as space_name,
                guests.id as guest_id,
                guests.username as guest_username,
                booking_message,
                status,
                hosts.id as host_id
            from booking_requests
            join bookings on booking_id=bookings.id
            join spaces on bookings.space_id=spaces.id
            join users guests on guest_id = guests.id
            join users hosts on spaces.user_id = hosts.id
            where hosts.id = %s;
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
