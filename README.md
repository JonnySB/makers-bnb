# makers-bnb

## About

Initially started as a group project with 5 other developers on the Makers
Software Engineering Bootcamp, and later taken further as a way to experiment
with additional Flask concepts myself, makers-bnb started life as an
opportunity to learn about managing source control when working as part of an
engineering team (i.e. creating feature branches, pull requests, holding code
reviews and ultimately merging to main). In addition, having started with user
stories, the project provided an opportunity to plan how a team can approach a
project such that all developers are able to remain productive. I.e. using
agile methodologies, converting user stories to tickets (creating vertical
slices of work to avoid inter-feature dependencies and blocking) and agreeing
important information ( such as variable naming, database structure etc.)
beforehand.

After the week long project, I decided to continue building out the project to
include a database backed booking management system, and to incorporate
functionality to handle additional data types (such as image uploads). I also
spent considerable time refactoring the project and writing tests to improve
test coverage, readability and maintainablility.

## Project Setup

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

## Things you could try:

- Install the project and run the testing suit. (Instructions found in the project setup section)
