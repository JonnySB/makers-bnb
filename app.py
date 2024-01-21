import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection
from lib.space import *
from lib.space_repository import *
from lib.booking_request import BookingRequest
from lib.booking_request_repository import BookingRequestRepository
from lib.user import User
from lib.user_repository import UserRepository
from lib.booking import Booking
from lib.booking_repository import BookingRepository
from lib.booking_request_manager_repository import BookingRequestManagerRepository
from datetime import datetime, timedelta

# Create a new Flask app
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# == HELPER METHODS ==


# Gets user id from active session and used it to return corresponding User
# object. If user session not active, return None
def get_user_from_session_details(connection) -> User | None:
    user_repository = UserRepository(connection)
    user_id = session.get("user_id", None)
    user = None
    if user_id != None:
        user = user_repository.get_user_by_id(user_id)
    return user


# == USER CREATE / LOGIN / LOGOUT ROUTES ==


# render signup template
@app.route("/signup", methods=["GET"])
def get_user_info():
    return render_template("user_signup.html")


# If signup template completed correctly (password correctly confirmed), create
# user, add to database and redirect to login page. If passwords not confirmed
# then re-render user_signup template with associated error message.
@app.route("/add_user", methods=["POST"])
def add_user_to_db():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]
    if password == confirm_password:
        # user id will be overwritten by db id
        user = User(1, username, email, password)
        user = user_repository.add_user_to_db(user)
        return redirect("/login")
    else:
        return render_template(
            "user_signup.html", errors="Please ensure your details are correct"
        )


# If 'GET', render login template and collect details.
# if 'POST', check details and create session with associated user_id and
# logged_in bool, and then redirect to spaces
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
        user_id = user_repository.check_username_or_email_and_password(
            username, password
        )

        if not user_id:
            return render_template("login.html", errors="Incorrect login details")

        # update session variables to indicate logged in
        session["user_id"] = user_id
        session["logged_in"] = True

        return redirect("/spaces")


# log user out and redirect to spaces
@app.route("/logout", methods=["GET"])
def logout_user():
    session["user_id"] = None
    session["logged_in"] = False
    return redirect(f"/spaces")


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


# Render homepage (spaces), with additional session/ user information if
# logged in
@app.route("/spaces", methods=["GET"])
def get_spaces():
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)

    spaces = space_repo.get_all_spaces()

    logged_in = session.get("logged_in", False)
    user = get_user_from_session_details(connection)

    return render_template(
        "spaces/spaces.html", spaces=spaces, logged_in=logged_in, user=user
    )


# See inside route for GET/ POST
# If GET - Render new space form if user logged in, otherwise redirect to signup
# If POST - extract space / booking information and add records to db
@app.route("/spaces/new", methods=["GET", "POST"])
def create_space():
    if request.method == "GET":
        connection = get_flask_database_connection(app)

        logged_in = session.get("logged_in", False)
        # ensure user logged in if visits by link
        if not logged_in:
            return redirect("/signup")

        user = get_user_from_session_details(connection)

        return render_template("spaces/new.html", logged_in=logged_in, user=user)

    else:
        connection = get_flask_database_connection(app)
        space_repository = SpaceRepository(connection)
        booking_repository = BookingRepository(connection)

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        available_from = request.form["available_from"]
        available_to = request.form["available_to"]

        user = get_user_from_session_details(connection)
        # redirect to login if session expires
        if user is None:
            return redirect("/login")

        space = Space(None, name, description, float(price), user.id)
        space = space_repository.add_space_to_db(space)

        available_from = datetime.strptime(available_from, "%Y-%m-%d")
        available_to = datetime.strptime(available_to, "%Y-%m-%d")
        current_date = available_from

        while current_date <= available_to:
            booking = Booking(None, current_date, True, space.id)
            booking = booking_repository.add_booking_to_db(booking)
            current_date += timedelta(days=1)

        return redirect(f"/spaces")


# Render associated space details template
@app.route("/spaces/<id>", methods=["GET"])
def get_space(id):
    connection = get_flask_database_connection(app)
    space_repo = SpaceRepository(connection)
    booking_repo = BookingRepository(connection)
    space = space_repo.get_space_by_id(id)
    bookings = booking_repo.get_bookings_by_space_id(id)

    logged_in = session.get("logged_in", False)
    user_details = get_user_from_session_details(connection)

    return render_template(
        "space.html",
        space=space,
        bookings=bookings,
        logged_in=logged_in,
        user=user_details,
    )


# If GET - check logged in and render make booking template
# If POST - get booking message from previous form and add booking request to
# db. Set booking availability to False and redirect to homepage (spaces)
@app.route("/spaces/rent/<booking_id>/<space_id>", methods=["GET", "POST"])
def rent_space(booking_id, space_id):
    connection = get_flask_database_connection(app)
    logged_in = session.get("logged_in", False)

    # url cannot be called directly when not logged in
    if not logged_in:
        return redirect("/login")
    user_details = get_user_from_session_details(connection)

    booking_details = {"booking_id": booking_id, "space_id": space_id}

    if request.method == "GET":
        return render_template(
            "make_booking.html",
            logged_in=logged_in,
            user=user_details,
            booking_details=booking_details,
        )
    else:
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
    user_details = get_user_from_session_details(connection)
    # redirect to login if session expires
    if user_details is None:
        return redirect("/login")

    booking_request_manager_repository = BookingRequestManagerRepository(connection)

    booking_requests = booking_request_manager_repository.get_BRM_by_host_id(
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

    boooking_request_manager = booking_req_man_repo.get_BRM_by_booking_request_id(
        booking_request_id
    )

    all_related_booking_request_ids = (
        booking_req_man_repo.get_booking_request_ids_by_booking_id(
            boooking_request_manager.booking_id
        )
    )

    for id in all_related_booking_request_ids:
        if str(id) == str(booking_request_id):
            booking_req_man_repo.set_booking_request_status_to_accepted(
                booking_request_id
            )
        else:
            booking_req_man_repo.set_booking_request_status_to_declined(id)

    boooking_request_manager = booking_req_man_repo.get_BRM_by_booking_request_id(
        booking_request_id
    )

    return redirect("/manage_requests/host")


# UNTESTED
@app.route("/manage_bookings/reject/<booking_request_id>", methods=["POST"])
def reject_booking_request(booking_request_id):
    connection = get_flask_database_connection(app)
    booking_req_man_repo = BookingRequestManagerRepository(connection)
    booking_req_man_repo.set_booking_request_status_to_declined(booking_request_id)

    return redirect("/manage_requests/host")


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5001)))
