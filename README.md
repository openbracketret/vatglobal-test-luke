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

-   Optionally you can also specify the compose file locally by doing:

        $ export COMPOSE_FILE=local.yml

    This will then allow you to run (NOTE: you no longer have the "-f" flag):

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

### Getting up and running without Docker
-   I do not recommend this method but it is completely possible to do this without Docker. I am going to assume that you have python 3.9 installed as well as PostgreSQL 12 or higher. Firstly you want to create a virtual environment that will be used to store all the packages that the project requires.

        $ python3.9 -m venv <path>
    
-   Then you want to activate it by running the following:

        $ source <path>/bin/activate

-   Now you will want to install all of the required packages

        $ pip install -r requirements/local.txt

-   Next we want to create the database for the project:

        $ createdb vatglobal_test -U postgres --password <password>

-   Set environment variables for running:

        $ export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/vatglobal_test
        $ export USE_DOCKER=no

-   Apply migrations:

        $ python manage.py migrate

-   Create a user:

        $ python manage.py createsuperuser

-   Run the server:

        $ python manage.py runserver

-   Run tests with:

        $ pytest

## Available endpoints and their params
All endpoints except the token retrieval endpoint require the **"Authorization"** header in the form **Token <token>**
### /auth-token/
This is a POST request with the following:

        username: <username>
        password: <password>

This will return the token for the related user.
### /processFile/
This is a POST request with the following:

        file: <file>

Where file is the file that you want to uploade and process, the endpoint expects a csv file

### /retrieveRows/
This is a GET request with the following params: (* = optional)

        country: <string>
        date: <string in format YYYY/MM/DD>
        *currency: <string>

This will return all rows inside of the database that match the specified paramaters. If currency is passed in it will handle changing the currencies with their related exchange rates
## Some Considerations

### The NONE country approach
In order to mitigate the effects of my poorly found csv's that are preloaded into the database in order to store a list of countries and their alpha codes and their currency codes I have manually created a "NONE" country which is close to the approach that Google takes with their "null island" on Google Maps.

### Being "cheap" on the provided API
In order to make sure that I was as cheap as possible with the provided API, I made a database entry that contained the from and to currency converstions that I would need. I then would be able to reuse those values for the next 30 minutes (I chose this in the case of long operations), after the 30 minutes had expired I would delete the entry and if I ever needed that converstion again I would simply do another lookup on the API for the conversion rate.

### Cookiecutter
In order to speed up the process of me starting the task and getting environments etc that were easy to use I used cookiecutter-django to build the project initially. This way I am given access by default to almost anything that I need. As per the specification I made sure to upgrade the version of Django that I am using (to 4.0.2).

### Shoddy testing
I have tried my best to test as much as I can and as best I can. Testing is the only thing that is my downfall because my exposure to testing and proper testing is not very vast.

### A more scalable solution 
Something that should be considered is that this solution is not very scalable as the "processFile" endpoint takes quite some time to process the information and then eventually store it in the database. A more scalable solution I think would be something that would use a message queue and send that information to a different perhaps micro-service or if the system that the current application is being hosted on is powerful enough to handle requests and processing you could use something like: Ingest the file from the upload without processing it and save it somewhere. Add a task to a message queue or to a system like huey that will queue the task to be done later. Once the request has returned you can start processing the file in the background. Possibly have an additional paramater that stores WHO has uploaded the file in the case that there is an error during processing the file then you can let the user that uploaded the file know that there has been an error. You could possibly even do some basic processing which is a much quicker task than inputting the information into the database before responding to the request in order to make sure the file format is correct and can be processed. Then after you've responded begin the database query (which I believe takes the most time).