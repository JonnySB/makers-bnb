from lib.booking import Booking


class BookingRepository:
    def __init__(self, connection):
        self._connection = connection

    # Returns all bookings associated with a particular space id as a list
    # of Booking objects, ordered by id
    def get_bookings_by_space_id(self, space_id: int) -> list[Booking]:
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE space_id = %s ORDER BY id",
            [space_id],
        )

        bookings = []
        for row in rows:
            bookings.append(
                Booking(
                    row["id"],
                    row["date"],
                    row["is_available"],
                    row["space_id"],
                )
            )

        return bookings

    # Using a booking_id, set a bookings availability to false in the database
    def set_booking_availability_to_false(self, booking_id: int):
        self._connection.execute(
            """
            UPDATE bookings
            SET is_available = FALSE
            WHERE id = %s
            """,
            [booking_id],
        )

    # Insert booking details into bookings table of database
    # return Booking object with updated id
    def add_booking_to_db(self, booking: Booking) -> Booking:
        rows = self._connection.execute(
            """
            INSERT INTO bookings 
            (date, is_available, space_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            [booking.date, booking.is_available, booking.space_id],
        )
        row = rows[0]
        booking.id = row["id"]
        return booking

    # Use id to get a specific booking from the db and return as Booking object
    def get_booking_by_id(self, booking_id: int) -> Booking:
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE id = %s;", [booking_id]
        )
        row = rows[0]
        return Booking(
            row["id"],
            row["date"],
            row["is_available"],
            row["space_id"],
        )
