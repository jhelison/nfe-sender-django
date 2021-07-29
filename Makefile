VERSION = $(shell (poetry version).split(' ')[1])
PROJECTNAME = nfe_sender

MANAGEPY = $(CURDIR)/$(PROJECTNAME)/manage.py

env:
	poetry shell

run:
	python $(MANAGEPY) runserver

migrate:
	python $(MANAGEPY) makemigrations
	python $(MANAGEPY) migrate

test:
	poetry run black .
	poetry run pytest -s -x --no-header -v
	