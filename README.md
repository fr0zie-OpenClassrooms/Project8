# Project 8: Pur Beurre program using OpenFoodFacts API

This Django project interacts with the OpenFoodFacts API in order to find a healthier food substitute according to the desired product.

You can check project details on [Trello](https://trello.com/b/JOw9Eyf6/project-8).

## Installation

Create a virtual environment with the [venv](https://docs.python.org/3/tutorial/venv.html) module to install the program:

```bash
python3 -m venv .venv
```

Then, activate the virtual environment:

```bash
.venv/Scripts/activate
```

Install the dependencies using the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip install -r requirements.txt
```

## Usage

### Creating and populating database

First, create the database using:

```bash
python manage.py migrate
```

Then, populate the database with OpenFoodFacts products:

```bash
python manage.py fill
```

### Application use

To start the server, run the following command:

```bash
python manage.py runserver
```

You can now access your local server on [localhost](http://localhost:8000/)

### Tests

This project uses [pytest](https://docs.pytest.org/en/6.2.x/) instead of default Django [unittest](https://docs.djangoproject.com/fr/4.0/topics/testing/overview/).

To start tests, run the following command:

```bash
pytest --cov
```

## License

[MIT](https://www.wikipedia.org/wiki/MIT_License)