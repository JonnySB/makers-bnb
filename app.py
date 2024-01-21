import os
from flask import Flask, request, render_template, redirect, session
from lib.booking_request import BookingRequest
from lib.booking_request_repository import BookingRequestRepository
from lib.database_connection import get_flask_database_connection
from lib.space_repository import *
from lib.space import *
from lib.user_repository import UserRepository
from lib.user import User
from lib.booking_repository import BookingRepository
from lib.booking import Booking
from lib.booking_request_manager_repository import BookingRequestManagerRepository
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
        # redirect to login if session expires
        if user_details is None:
            return redirect("/login")

        space = Space(None, name, description, price, user_details.id)
        space = space_repository.create(space)

        available_from = datetime.strptime(available_from, "%Y-%m-%d")
        available_to = datetime.strptime(available_to, "%Y-%m-%d")
        current_date = available_from

        while current_date <= available_to:
            booking = Booking(None, current_date, True, space.id)
            booking = booking_repository.add_booking_to_db(booking)
            current_date += timedelta(days=1)

        return redirect(f"/spaces")


@app.route("/spaces/<id>", methods=["GET"])
def get_space(id):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    booking_repo = BookingRepository(connection)
    space = space_repo.get_by_id(id)
    bookings = booking_repo.get_bookings_by_space_id(id)

    logged_in = session.get("logged_in", False)
    user_details = get_user_details(connection)

    return render_template(
        "space.html",
        space=space,
        bookings=bookings,
        logged_in=logged_in,
        user=user_details,
    )


@app.route("/spaces/rent/<booking_id>/<space_id>", methods=["GET", "POST"])
def rent_space(booking_id, space_id):
    connection = get_flask_database_connection(app)
    logged_in = session.get("logged_in", False)
    user_details = get_user_details(connection)
    # redirect to login if session expires
    if user_details is None:
        return redirect("/login")

    booking_details = {"booking_id": booking_id, "space_id": space_id}

    if request.method == "GET":
        return render_template(
            "make_booking.html",
            logged_in=logged_in,
            user=user_details,
            booking_details=booking_details,
        )
    else:
        # create booking request object
        booking_message = request.form["booking_message"]
        booking_request = BookingRequest(
            None, booking_id, user_details.id, booking_message, 1
        )

        # add to db
        booking_request_repository = BookingRequestRepository(connection)
        booking_request_repository.add_booking_request_to_db(booking_request)

        # potentially move the availability update to when request accepted
        booking_repo = BookingRepository(connection)
        booking_repo.set_booking_availability_to_false(booking_id)

    return redirect(f"/spaces/{space_id}")


# UNTESTED
@app.route("/manage_requests/host", methods=["GET"])
def manage_booking_requests():
    connection = get_flask_database_connection(app)
    logged_in = session.get("logged_in", False)
    user_details = get_user_details(connection)
    # redirect to login if session expires
    if user_details is None:
        return redirect("/login")

    booking_request_manager_repository = BookingRequestManagerRepository(connection)

    booking_requests = booking_request_manager_repository.get_by_host_id(
        user_details.id
    )

    return render_template(
        "manage_booking_requests.html",
        booking_requests=booking_requests,
        logged_in=logged_in,
        user=user_details,
    )


# UNTESTED
@app.route("/manage_bookings/accept/<booking_request_id>", methods=["POST"])
def accept_booking_request(booking_request_id):
    connection = get_flask_database_connection(app)
    booking_req_man_repo = BookingRequestManagerRepository(connection)

    boooking_request_manager = booking_req_man_repo.get_by_booking_request_id(
        booking_request_id
    )

    all_related_booking_request_ids = (
        booking_req_man_repo.get_all_related_booking_request_ids(
            boooking_request_manager.booking_id
        )
    )

    for id in all_related_booking_request_ids:
        if str(id) == str(booking_request_id):
            booking_req_man_repo.accept_booking(booking_request_id)
        else:
            booking_req_man_repo.reject_booking(id)

    boooking_request_manager = booking_req_man_repo.get_by_booking_request_id(
        booking_request_id
    )

    return redirect("/manage_requests/host")


# UNTESTED
@app.route("/manage_bookings/reject/<booking_request_id>", methods=["POST"])
def reject_booking_request(booking_request_id):
    connection = get_flask_database_connection(app)
    booking_req_man_repo = BookingRequestManagerRepository(connection)
    booking_req_man_repo.reject_booking(booking_request_id)

    return redirect("/manage_requests/host")


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
