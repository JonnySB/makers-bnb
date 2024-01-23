from playwright.sync_api import Page, expect
from lib.user_repository import UserRepository
from lib.user import User
from app import *
import time
import os
import pytest


# test spaces elements are rendered correctly on spaces page
def test_get_spaces(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    name_element = page.locator(".t-space-name")
    expect(name_element).to_have_text(
        [
            "Enchanted Retreat",
            "Urban Oasis Loft",
            "Sunset Serenity Cottage",
            "Luxury Skyline Penthouse",
            "Seaside Bliss Villa",
        ]
    )
    description_element = page.locator(".t-space-description")
    expect(description_element).to_have_text(
        [
            "Discover the magic of this hidden gem. A cozy haven surrounded by nature, perfect for a peaceful escape.",
            "Experience city living at its finest. Our modern loft offers stunning views and all the amenities you need for a stylish stay.",
            "Unwind in our charming cottage with breathtaking sunset views. A tranquil setting for a memorable getaway.",
            "Indulge in luxury high above the city. Our penthouse boasts panoramic skyline views and top-notch amenities.",
            "Escape to paradise in our seaside villa. Relax to the sound of waves and enjoy the ultimate beachfront experience.",
        ]
    )
    price_element = page.locator(".t-space-price")
    expect(price_element).to_have_text(["£130.00/ night" for _ in range(5)])


# test that when space 3's details are clicked, we see the correct infomation
# for that space rendered on a details page
def test_view_space_details_page(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    page.click("a[href='/spaces/3']")
    name_element = page.locator(".t-space-name")
    expect(name_element).to_have_text("Sunset Serenity Cottage")
    description_element = page.locator(".t-space-description")
    expect(description_element).to_have_text(
        "Unwind in our charming cottage with breathtaking sunset views. A tranquil setting for a memorable getaway."
    )
    price_element = page.locator(".t-space-price")
    expect(price_element).to_have_text("£130.00/ night")
    date_element = page.locator(".t-space-date")
    expect(date_element).to_have_text(["2024-05-10", "2024-05-11", "2024-05-12"])
    availability_element = page.locator(".t-space-availability")
    expect(availability_element).to_have_text(["Available", "Available", "Available"])


# SKIPPED
# Test that when a new space is created, the associated space is then rendered
# on the spaces page.
@pytest.mark.skip
def test_create_space(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")

    # login
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name='user']", "user1")
    page.fill("input[name='password']", "Password")
    page.click("input[type='submit']")

    # List a space
    page.click("a[href='/spaces/new']")
    file_path = os.path.join(os.getcwd(), "../static/test_images/test_image.jpg")
    page.set_input_files('input[type="file"]', file_path)

    page.fill("input[name='name']", "TestName")
    page.fill("input[name='description']", "Test Description")
    page.fill("input[name='price']", "100")
    page.fill("input[name='available_from']", "2024-03-26")
    page.fill("input[name='available_to']", "2024-03-29")
    page.screenshot(path="screenshot.png")
    page.click("button[id='button-submit']")

    # rendering blank page here instead of spaces
    name_element = page.locator(".t-space-name")
    expect(name_element).to_have_text(
        [
            "Enchanted Retreat",
            "Urban Oasis Loft",
            "Sunset Serenity Cottage",
            "Luxury Skyline Penthouse",
            "Seaside Bliss Villa",
            "Test Name",
        ]
    )
    description_element = page.locator(".t-space-description")
    expect(description_element).to_have_text(
        [
            "Discover the magic of this hidden gem. A cozy haven surrounded by nature, perfect for a peaceful escape.",
            "Experience city living at its finest. Our modern loft offers stunning views and all the amenities you need for a stylish stay.",
            "Unwind in our charming cottage with breathtaking sunset views. A tranquil setting for a memorable getaway.",
            "Indulge in luxury high above the city. Our penthouse boasts panoramic skyline views and top-notch amenities.",
            "Escape to paradise in our seaside villa. Relax to the sound of waves and enjoy the ultimate beachfront experience.",
            "Test Description",
        ]
    )
    price_element = page.locator(".t-space-price")
    expect(price_element).to_have_text(
        ["£130.00/ night" for _ in range(5)] + ["£100.00/ night"]
    )
    page.click("a[href='/spaces/6']")
    date_element = page.locator(".t-space-date")
    expect(date_element).to_have_text(
        ["2024-03-26", "2024-03-27", "2024-03-28", "2024-03-29"]
    )


# Test when a user is created, that the user is then created in the users table
# of the db
def test_create_user(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/signup")

    page.fill("input[name=username]", "user6")
    page.fill("input[name=email]", "user6@user.com")
    page.fill("input[name=password]", "Password")
    page.fill("input[name=confirm_password]", "Password")

    page.click("text='Sign Up'")

    repository = UserRepository(db_connection)

    users = repository.get_all_users()
    assert users == [
        User(1, "user1", "user1@user.com", "Password"),
        User(2, "user2", "user2@user.com", "Password"),
        User(3, "user3", "user3@user.com", "Password"),
        User(4, "user4", "user4@user.com", "Password"),
        User(5, "user5", "user5@user.com", "Password"),
        User(6, "user6", "user6@user.com", "Password"),
    ]


# test user is able to login and view their booking requests from a host
# perspective
def test_login_and_view_booking_requests(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    page.click("text=My Bookings")
    page.fill("input[name=user]", "user1")
    page.fill("input[name=password]", "Password")
    page.click("text='Sign In'")
    page.click("text=My Bookings")
    booking_messages = page.locator("td.testing-locator")
    expect(booking_messages).to_have_text([])


# test user is able to login and view their booking requests from a host
# perspective and accept a booking
def test_accept_booking_request(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    page.click("text=My Bookings")
    page.fill("input[name=user]", "user1")
    page.fill("input[name=password]", "Password")
    page.click("text='Sign In'")
    page.click("text=My Bookings")

    page.click("text='Accept'")
    accepted_username = page.locator("td.accepted-guest-username")
    expect(accepted_username).to_have_text("user1")


# test user is able to login and view their booking requests from a host
# perspective and accept a booking
def test_decline_booking_request(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    page.click("text=My Bookings")
    page.fill("input[name=user]", "user1")
    page.fill("input[name=password]", "Password")
    page.click("text='Sign In'")
    page.click("text=My Bookings")

    page.click("text='Reject'")
    rejected_username = page.locator("td.rejected-guest-username")
    expect(rejected_username).to_have_text("user1")


# test user is able to login and make booking request as a guest
def test_make_booking_request(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    page.click("text=My Bookings")
    page.fill("input[name=user]", "user1")
    page.fill("input[name=password]", "Password")
    page.click("text='Sign In'")

    page.click("a[href='/spaces/1']")
    available_date = page.locator("h6.available")
    expect(available_date).to_have_text("2024-05-12")

    page.click("h6.available")

    page.fill("input[name=booking_message]", "Please can I stay?")
    page.click("text='Submit booking request'")

    unavailable_date = page.locator("h6.unavailable")
    expect(unavailable_date).to_have_text(["2024-05-10", "2024-05-11", "2024-05-12"])
