from lib.user import User
import bcrypt


class UserRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        users = []
        rows = self.connection.execute("SELECT * FROM users")

        for row in rows:
            user = User(row["id"], row["username"], row["email"], "None")
            users.append(user)
        return users

    def create(self, user):
        self.connection.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)",
            [user.username, user.email, user.hashed_password],
        )

    def get_user_id(self, user):
        """Get user id from database if exists, otherwise return False"""
        rows = self.connection.execute(
            "SELECT * from users WHERE username = %s OR email = %s", [user, user]
        )
        if len(rows) == 0:
            return False
        row = rows[0]
        return row["id"]

    def check_user_valid(self, username, password):
        """
        Check if username/ email and password are valid, retuen user_id if
        True, otherwise False
        """
        users_id = self.get_user_id(username)
        if not users_id:
            return False

        hashed_database_pw = self.connection.execute(
            "SELECT hashed_password from users WHERE id = %s", [users_id]
        )[0]["hashed_password"]
        is_valid_password = bcrypt.checkpw(password.encode("utf-8"), hashed_database_pw)

        if is_valid_password:
            return users_id
        return False

    def get_by_id(self, user_id):
        rows = self.connection.execute("SELECT * FROM users WHERE id = %s", [user_id])[
            0
        ]
        user = User(rows["id"], rows["username"], rows["email"], "None")
        return user
