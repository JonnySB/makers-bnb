class BookingRequestManager:
    # UNTESTED
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
        self.set_status(status_num)
        self.host_id = host_id

    # UNTESTED
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # UNTESTED
    def __repr__(self):
        return f"BookingRequest: {self.booking_request_id}, {self.booking_id}, {self.space_name}, {self.guest_id}, {self.guest_username}, {self.booking_date}, {self.booking_message}, {self.status}, {self.host_id}"

    # UNTESTED
    def set_status(self, status_num):
        if status_num == 1:
            self.status = "Pending"
        elif status_num == 2:
            self.status = "Accepted"
        else:
            self.status = "Declined"
