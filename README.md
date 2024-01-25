# MakersBnB

## What is MakersBnB?

MakersBnB is a limited-functionality copy of the concept behind the AirBnB
platform. The predominant focus was on using Python and Flask to create a
website that, coupled with a postgres back-end, is able to persist data and
inject it into the static html pages using the jinja template engine. Bootstrap
was used to create a basic UI, however, this was not the focus of the website.

![Homepage](/static/readme_images/homepage.png)

## How was MakersBnB developed?

MakersBnB started life as a group project with 5 other developers on the Makers
Software Engineering Bootcamp. However, upon delivering the MVP, I opted to
continue working on the project myself as an opportunity to experiment with
additional flask features / concepts.

## What did I learn about throughout this project?

### Group work section:

- Managing source control across multiple feature branches. I.e. branching, re-basing with any updates, pull requests, code reviews, merge requests etc.
- Project planning: creating non-blocking streams of work such that we maintained developer productivity. I.e planning vertical slices such that dependencies were reduced
- Agile methodology - sprint planning, stand-ups, retros etc.
- Ensuring agreement upfront on key classes, attributes, methods, variable names and database structure

### Personal technical skills development:

- Refactoring to improve readability / maintainability
- Database planning and design - database schema development
- Postgres - Database creation, SQL queries, testing seed development
- Software architecture - planning app structure, classes, objects etc.
- Flask framework - Model Repositories, Model Objects, Routing, passing form data etc.
- Test Driven Development (pytest, playwright, mocking etc.)
- Authentication
- HTML templating with Jinja template engine
- CSS / Bootstrap

# Can I run MakersBnB myself?

Yes! Please follow the instructions below to get set up, and if you like you
could try a few of the options in the 'Things you could try' section to see what
the project is capable of.

```shell
# Clone the repository to your local machine
; git clone https://github.com/JonnySB/makers-007-engineering-project-1.git

; cd makers-007-engineering-project-1

# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Install the virtual browser we will use for testing
; playwright install
# If you have problems with the above, contact your coach

# Create a test and development database (This assumes you have postgres)
; createdb MAKERS_BNB
; createdb MAKERS_BNB_test

# Seed the development database (ensure you have run `pipenv shell` first)
; python seed_dev_database.py

# Run the tests (with extra logging)
; pytest -sv

# Run the app
; python app.py

#Visit http://localhost:5001/spaces in your browser
```

## What could I try when running MakersBnB?

- Install the project and run the testing suite. (Instructions found in the 'Can I run MakersBnB myself?' section above
- Navigate the website whilst not logged in - notice some areas of the website / actions are restricted whilst not authenticated
- Sign-up as a user and log in.
  - Note, if you would rather log in as an existing test user, please use username: 'user1' through 'user5', password:'Password')
- (While logged in) List a space and some dates it is available to book (List a space button on homepage)
- (While logged in) Make a booking request for a space for a night (Click on a space from the home page, go into its details area and click on an available date)
  - Note, if you do this for a space the logged in user created, you will be able to see / approve / reject this request in the booking area.
- (While logged in) Navigate to 'Manage my bookings' and see all your booking requests both as Host and Guest under their respective sections.
- (While logged in) Approve / Decline etc. some bookings in the Host booking area. Note, this will be updated for the Guest in their respective booking area.
- (While logged in) Cancel a booking request in the Guest booking area. This will remove the request from the system all together.

## Images and planning materials:

Database Schema - database normalisation taken into account:
![Database Schema](/static/readme_images/database_schema.png)

### The following is a non-exhaustive set of images from accross the website.

An area to manage your bookings:
![Manage my bookings](/static/readme_images/manage_my_bookings.png)

An area to sign-up a new user:
![User sign up](/static/readme_images/user_sign_up.png)

An area to make a booking request:
![Space details page](/static/readme_images/space_details_page.png)
