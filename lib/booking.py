class Booking:
    def __init__(self, id, date, is_available, space_id):
        self.id = id
        self.date = date
        self.is_available = is_available
        self.space_id = space_id

    # ensure two object with identical attrs will be found equal
    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    # return nicely formatted string version of Booking object
    def __repr__(self) -> str:
        return f"Booking({self.id}, {self.date}, {self.is_available}, {self.space_id})"
