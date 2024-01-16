class BookingRequest:
    def __init__(self, id, booking_id, guest_id, booking_message, status_num):
        self.id = id
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.booking_message = booking_message
        self.set_status(status_num)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"BookingRequest: {self.id}, {self.booking_id}, {self.guest_id}, {self.booking_message}, {self.status}"

    def set_status(self, status_num):
        if status_num == 1:
            self.status = "Pending"
        elif status_num == 2:
            self.status = "Accepted"
        else:
            self.status = "Declined"
