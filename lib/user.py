import bcrypt


class User:
    def __init__(self, id: int | None, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.hashed_password = self._hash_password(password)

    # ensure two object with identical attrs will be found equal
    def __eq__(self, other):
        # return self.__dict__ == other.__dict__
        return all(
            [
                self.id == other.id,
                self.email == other.email,
                self.username == other.username,
            ]
        )

    # return nicely formatted string version of User object
    def __repr__(self):
        return f"User: {self.id}, {self.username}, {self.email}"

    # When called with a plain text password, a hashed password is returned
    def _hash_password(self, password):
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt)
        return password_hash
