VERSION = $(shell (poetry version).split(' ')[1])
PROJECTNAME = nfe_sender

MANAGEPY = $(CURDIR)/$(PROJECTNAME)/manage.py
DATABASE = $(CURDIR)/$(PROJECTNAME)/db.sqlite3

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

superuser:
	python ./nfe_sender/manage.py createsuperuser

# $(wildcard ../Test/*/.)

reset:
	pwsh -noprofile -command if(Test-Path $(DATABASE)) {Remove-Item $(DATABASE)}
	pwsh -noprofile -command (Get-ChildItem -Recurse | Where-Object {$_.Name.EndsWith("migrations")}).fullname | Remove-Item -Recurse -Exclude __init__.py