VERSION = $(shell (poetry version).split(' ')[1])
PROJECTNAME = nfe_sender

MANAGEPY = $(CURDIR)/$(PROJECTNAME)/manage.py
DATABASE = $(CURDIR)/$(PROJECTNAME)/db.sqlite3

MIGRATIONS =  $(sort $(dir $(wildcard ../migrations/*/)))

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
	powershell if(Test-Path $(DATABASE)) {Remove-Item $(DATABASE)}

	powershell $var = Get-ChildItem -Recurse | Where-Object { $_.PSIsContainer -and $_.Name.EndsWith("migrations")}

for Get-ChildItem -Recurse | Where-Object { $_.PSIsContainer -and $_.Name.EndsWith("migrations")}

Get-ChildItem -Recurse | Where-Object {$_.Name.EndsWith("migrations")} | echo