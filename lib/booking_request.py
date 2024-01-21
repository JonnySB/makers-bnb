class BookingRequest:
    def __init__(
        self,
        id: int,
        booking_id: int,
        guest_id: int,
        booking_message: str,
        status_num: int,
    ):
        self.id = id
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.booking_message = booking_message
        self.set_status(status_num)

    # ensure two object with identical attrs will be found equal
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # return nicely formatted string version of Booking object
    def __repr__(self) -> str:
        return f"BookingRequest: {self.id}, {self.booking_id}, {self.guest_id}, {self.booking_message}, {self.status}"

    # takes int from database and assigns it to its associated status. I.e.
    # 1: pending, 2: accepted, 3: declined
    def set_status(self, status_num: int):
        if status_num == 1:
            self.status = "Pending"
        elif status_num == 2:
            self.status = "Accepted"
        else:
            self.status = "Declined"
