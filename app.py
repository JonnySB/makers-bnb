import os
from flask import Flask, request, render_template, redirect, session
from lib.booking_request_repository import BookingRequestRepository
from lib.database_connection import get_flask_database_connection
from lib.space_repository import *
from lib.space import *
from lib.user_repository import UserRepository
from lib.user import User
from lib.booking_repository import BookingRepository
from lib.booking import Booking
from datetime import datetime, timedelta

# Create a new Flask app
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# == Helper Methods ==
def get_user_details(connection):
    user_repo = UserRepository(connection)
    user_id = session.get("user_id", None)
    user_details = None
    if user_id != None:
        user_details = user_repo.get_by_id(user_id)
    return user_details


# == User Create / Login / Logout Routes ==
@app.route("/signup", methods=["GET"])
def get_user_info():
    return render_template("user_signup.html")


@app.route("/add_user", methods=["POST"])
def add_user_to_db():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    # confirm_password

    user = User(None, username, email, password)

    user = user_repository.create(user)
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    else:
        connection = get_flask_database_connection(app)
        user_repository = UserRepository(connection)

        username = request.form["user"]  # both username or email valid options
        password = request.form["password"]

        # returns user_id if valid, False otherwise
        user_id = user_repository.check_user_valid(username, password)

        if not user_id:
            return render_template("login.html", errors="Incorrect login details")

        # update session variables to indicate logged in
        session["user_id"] = user_id
        session["logged_in"] = True

        return redirect("/spaces")


@app.route("/logout", methods=["GET"])
def logout_user():
    session["user_id"] = None
    session["logged_in"] = False
    return redirect(f"/spaces")


# == unauthenticated routes ==


# for development purposes only - easy reseeding:
@app.route("/reseed")
def reseed_database():
    connection = get_flask_database_connection(app)
    connection.connect()
    connection.seed("seeds/makers_bnb.sql")
    return redirect("/spaces")


# Homepage redirect
@app.route("/")
def set_default_route():
    return redirect("/spaces")


# Homepage
@app.route("/spaces", methods=["GET"])
def get_spaces():
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)

    spaces = space_repo.all()

    logged_in = session.get("logged_in", False)
    user_details = get_user_details(connection)

    return render_template(
        "spaces/spaces.html", spaces=spaces, logged_in=logged_in, user=user_details
    )


@app.route("/spaces/new", methods=["GET", "POST"])
def create_space():
    if request.method == "GET":
        connection = get_flask_database_connection(app)

        logged_in = session.get("logged_in", False)
        user_details = get_user_details(connection)

        return render_template(
            "spaces/new.html", logged_in=logged_in, user=user_details
        )

    else:
        connection = get_flask_database_connection(app)
        space_repository = SpaceRepository(connection)
        booking_repository = BookingRepository(connection)

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        available_from = request.form["available_from"]
        available_to = request.form["available_to"]

        user_details = get_user_details(connection)

        space = Space(None, name, description, price, user_details.id)
        space = space_repository.create(space)

        available_from = datetime.strptime(available_from, "%Y-%m-%d")
        available_to = datetime.strptime(available_to, "%Y-%m-%d")
        current_date = available_from

        while current_date <= available_to:
            booking = Booking(None, current_date, True, space.id)
            booking = booking_repository.create(booking)
            current_date += timedelta(days=1)

        return redirect(f"/spaces")


@app.route("/spaces/<id>", methods=["GET"])
def get_space(id):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    booking_repo = BookingRepository(connection)
    space = space_repo.get_by_id(id)
    bookings = booking_repo.get_by_space_id(id)

    logged_in = session.get("logged_in", False)
    user_details = get_user_details(connection)

    return render_template(
        "space.html",
        space=space,
        bookings=bookings,
        logged_in=logged_in,
        user=user_details,
    )


@app.route("/spaces/rent/<booking_id>/<space_id>", methods=["GET"])
def rent_space(booking_id, space_id):
    connection = get_flask_database_connection(app)
    booking_repo = BookingRepository(connection)
    booking_repo.update_availability(booking_id)
    return redirect(f"/spaces/{space_id}")


@app.route("/manage_requests/host", methods=["GET"])
def manage_booking_requests():
    connection = get_flask_database_connection(app)
    booking_request_repository = BookingRequestRepository(connection)

    logged_in = session.get("logged_in", False)
    user_details = get_user_details(connection)

    booking_requests = booking_request_repository.get_by_host_id(user_details.id)

    users = UserRepository(connection)
    bookings = BookingRepository(connection)
    spaces = SpaceRepository(connection)

    booking_request_details = []
    for booking_request in booking_requests:
        guest = users.get_by_id(booking_request.guest_id)
        booking = bookings.get_by_booking_id(booking_request.booking_id)
        space = spaces.get_by_id(booking.space_id)
        host = users.get_by_id(space.user_id)
        booking_request_details.append([booking_request, guest, booking, space, host])

    return render_template(
        "manage_booking_requests.html",
        booking_requests=booking_request_details,
        logged_in=logged_in,
        user=user_details,
    )


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
