class BookingRequest:
    def __init__(self, id, booking_id, guest_id, booking_message, status):
        self.id = id
        self.booking_id = booking_id
        self.guest_id = guest_id
        self.booking_message = booking_message
        self.status = status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Space: {self.id}, {self.booking_id}, {self.guest_id}, {self.booking_message}, {self.status}"
