class Space:
    def __init__(
        self, id: int | None, name: str, description: str, price: float, user_id: int
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.user_id = user_id

    # ensure two object with identical attrs will be found equal
    def __eq__(self, other) -> bool:
        return self.__dict__ == other.__dict__

    # return nicely formatted string version of Space object
    def __repr__(self) -> str:
        return f"Space: {self.id}, {self.name}, {self.description}, {self.price}, {self.user_id}"
