class BookingRequestManager:
    def __init__(
        self,
        booking_request_id,
        booking_id,
        space_name,
        guest_id,
        guest_username,
        booking_date,
        booking_message,
        status_num,
        host_id,
    ):
        self.booking_request_id = booking_request_id
        self.booking_id = booking_id
        self.space_name = space_name
        self.guest_id = guest_id
        self.guest_username = guest_username
        self.booking_date = booking_date
        self.booking_message = booking_message
        self.convert_status_num_to_str_repr(status_num)  # -> self.status
        self.host_id = host_id

    # ensure two object with identical attrs will be found equal
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # return nicely formatted string version of BookingRequestManager object
    def __repr__(self) -> str:
        return f"BookingRequest: {self.booking_request_id}, {self.booking_id}, {self.space_name}, {self.guest_id}, {self.guest_username}, {self.booking_date}, {self.booking_message}, {self.status}, {self.host_id}"

    # takes int from database and assigns it to its associated status. I.e.
    # 1: pending, 2: accepted, 3: declined
    def convert_status_num_to_str_repr(self, status_num: int):
        if status_num == 1:
            self.status = "Pending"
        elif status_num == 2:
            self.status = "Accepted"
        else:
            self.status = "Declined"
