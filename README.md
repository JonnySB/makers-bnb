# MakersBnB

## What is MakersBnB?

MakersBnB is a limited-functionaity copy of the concept behind the AirBnB
platform. The predominant focus was on using Python and Flask to create a
website that, coupled with a postgres backend, is able to persist data and
inject it into the static html pages using the jinja template engine. To
create a basic UI, a bootstrap theme was used.

![Homepage](/static/readme_images/homepage.png)

## How was MakersBnB developed?

Initially started as a group project with 5 other developers on the Makers
Software Engineering Bootcamp, and later taken further as a way to experiment
with additional Flask concepts myself, MakersBnB started life as an
opportunity to learn about managing source control when working as part of an
engineering team (i.e. creating feature branches, pull requests, holding code
reviews and ultimately merging to main). In addition, having started with user
stories, we planned our work such that all developers were able to remain
productive. I.e. using agile methodologies, converting user stories to tickets
(creating vertical slices of work to avoid inter-feature dependencies and
blocking) and agreeing important information ( such as variable naming,
database structure etc.) beforehand.

After the week long project, I decided to continue building out the project to
include a database backed booking management system, and to incorporate
functionality to handle additional data types (such as image uploads). I also
spent considerable time refactoring the project and writing tests to improve
test coverage, readability and maintainablility.

## Can I run MakersBnB myself?

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

## What should I do when running MakersBnB?

- Install the project and run the testing suit. (Instructions found in the project setup section)

## Images and planning materials:
