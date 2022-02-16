# VatGlobal Test

The test assignment for VATGlobal

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Basic Commands

### Running locally with docker
-   The easiest way to run the system is to use docker. In order for that to work you will need to have Docker installed as well as docker-compose.

-   To build the stack you will want to run the following command:

        $ docker-compose -f local.yml build

-   To run the stack you will want to run:

        $ docker-compose -f local.yml up

-   You can also specify the compose file locally by doing:

        $ export COMPOSE_FILE=local.yml

    This will then allow you to run:

        $ docker-compose up

    And if you wish to run in detached mode you can use

        $ docker-compose up -d

-   Building and running the stack **should** automatically run the migrations on the database. If for some reason it does not you can execute the following to apply migrations:

        $ docker-compose -f local.yml run --rm django python manage.py migrate

    And then to create your super user you can use:

        $ docker-compose -f local.yml run --rm django python manage.py createsuperuser

### Running tests with docker

-   Running tests using docker is as simple as the previous commands:

        $ docker-compose -f local.yml run --rm django pytest


### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy vatglobal_test

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

## Some Considerations

### Being "cheap" on the provided API
In order to make sure that I was as cheap as possible with the provided API, I made a database entry that contained the from and to currency converstions that I would need. I then would be able to reuse those values for the next 30 minutes (I chose this in the case of long operations), after the 30 minutes had expired I would delete the entry and if I ever needed that converstion again I would simply do another lookup on the API for the conversion rate.

### Cookiecutter
In order to speed up the process of me starting the task and getting environments etc that were easy to use I used cookiecutter-django to build the project initially. This way I am given access by default to almost anything that I need. As per the specification I made sure to upgrade the version of Django that I am using (to 4.0.2).

### Shoddy testing
I have tried my best to test as much as I can and as best I can. Testing is the only thing that is my downfall because my exposure to testing and proper testing is not very vast.

### A more scalable solution 
Something that should be considered is that this solution is not very scalable as the "processFile" endpoint takes quite some time to process the information and then eventually store it in the database. A more scalable solution I think would be something that would use a message queue and send that information to a different perhaps micro-service or if the system that the current application is being hosted on is powerful enough to handle requests and processing you could use something like: Ingest the file from the upload without processing it and save it somewhere. Add a task to a message queue or to a system like huey that will queue the task to be done later. Once the request has returned you can start processing the file in the background. Possibly have an additional paramater that stores WHO has uploaded the file in the case that there is an error during processing the file then you can let the user that uploaded the file know that there has been an error. You could possibly even do some basic processing which is a much quicker task than inputting the information into the database before responding to the request in order to make sure the file format is correct and can be processed. Then after you've responded begin the database query (which I believe takes the most time).