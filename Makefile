VERSION = $(shell (poetry version).split(' ')[1])
PROJECTNAME = nfe_sender

MANAGEPY = $(CURDIR)/$(PROJECTNAME)/manage.py

env:
	shell C:/Users/jheli/AppData/Local/pypoetry/Cache/virtualenvs/nfe-sender-django-QEaoWS5b-py3.9/Scripts/Activate.ps1

start:
	python $(MANAGEPY) runserver

migrate:
	python $(MANAGEPY) makemigrations
	python $(MANAGEPY) migrate

test:
	poetry run black .
	poetry run pytest -x -s
	