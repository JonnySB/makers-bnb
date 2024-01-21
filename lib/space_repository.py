from lib.space import Space


class SpaceRepository:
    def __init__(self, connection):
        self._connection = connection

    # When called, all spaces are returned as Space objects
    def get_all_spaces(self) -> list[Space]:
        rows = self._connection.execute("SELECT * FROM spaces")
        spaces = []
        for row in rows:
            space = Space(
                row["id"], row["name"], row["description"], row["price"], row["user_id"]
            )
            spaces.append(space)
        return spaces

    # When called with a specific space id, a Space object object is returned
    # with the correct data
    def get_space_by_id(self, id: int) -> Space:
        rows = self._connection.execute("SELECT * FROM spaces where id=%s", [id])
        row = rows[0]
        return Space(
            row["id"], row["name"], row["description"], row["price"], row["user_id"]
        )

    # When called with a Space object, a corresponding record is created in the
    # database and the Space object's id field is updated to match the record
    def add_space_to_db(self, space: Space) -> Space:
        rows = self._connection.execute(
            """
            INSERT INTO spaces
            (name, description, price, user_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """,
            [space.name, space.description, space.price, space.user_id],
        )
        row = rows[0]
        space.id = row["id"]
        return space
