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

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
