# makers-bnb

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

# Create a test and development database
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
