.EXPORT_ALL_VARIABLES:
# .PHONY: venv help docker
# Unlike most variables, the variable SHELL is never set from the environment.
# This is because the SHELL environment variable is used to specify your personal
# choice of shell program for interactive use. It would be very bad for personal
# choices like this to affect the functioning of makefiles. See Variables from the Environment.
SHELL=/bin/bash
VIRTUAL_ENV ?= ${PWD}/.venv
SERVICE_NAME ?= db
# this part of the code gets the default POSTGRESQL_URL
# environment variable if exists and replaces it with default if not
ifdef POSTGRESQL_URL
POSTGRESQL_URL := $(POSTGRESQL_URL)
else
POSTGRESQL_URL := postgresql://postgres:password@127.0.0.1:5432/test_db?sslmode=disable
endif

# HEALTH CHECK
.ONESHELL:
check:
	@echo 1;

# RUN AND TEST HELPERS
.ONESHELL:
venv:
	rm -rf $(VIRTUAL_ENV) && python3.11 -m venv $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/pip3 install --upgrade pip wheel setuptools
	$(VIRTUAL_ENV)/bin/pip3 install --compile --upgrade --force-reinstall -r dev-requirements.txt
	$(VIRTUAL_ENV)/bin/pre-commit install

.ONESHELL:
test-app:
	$(VIRTUAL_ENV)/bin/pytest . -vv

.ONESHELL:
test-coverage:
	$(VIRTUAL_ENV)/bin/pytest . --cov

.ONESHELL:
flake8:
	$(VIRTUAL_ENV)/bin/flake8 .

.ONESHELL:
black:
	$(VIRTUAL_ENV)/bin/black .

.ONESHELL:
mypy:
	$(VIRTUAL_ENV)/bin/mypy .

# LOCAL POSTGRES INSTANCE
.ONESHELL:
docker-pull-db:
	@docker pull postgres:16.2-alpine

.ONESHELL:
docker-run-db: docker-pull-db
	@docker run --name test_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test_db -p 5432:5432 -d postgres:16.2-alpine

.ONESHELL:
docker-stop-db:
	@docker stop test_db

.ONESHELL:
docker-start-db:
	@docker start test_db

.ONESHELL:
docker-delete-db: docker-stop-db
	@docker rm test_db

# LOCAL REDIS INSTANCE
.ONESHELL:
docker-pull-redis:
	@docker pull redis:7.2.5-alpine

.ONESHELL:
docker-run-redis: docker-pull-redis
	@docker run --name test_redis -p 6379:6379 -d redis:7.2.5-alpine

.ONESHELL:
docker-stop-redis:
	@docker stop test_redis

.ONESHELL:
docker-start-redis:
	@docker start test_redis

.ONESHELL:
docker-delete-redis: docker-stop-redis
	@docker rm test_redis

# DB MIGRATIONS
.ONESHELL:
migrate-up:
	@migrate -verbose -database ${POSTGRESQL_URL} -path src/migrations up;

.ONESHELL:
migrate-down:
	@migrate -verbose -database ${POSTGRESQL_URL} -path src/migrations down 1;

.ONESHELL:
run-app:
	cd src && $(VIRTUAL_ENV)/bin/python -m uvicorn app:app --reload

.ONESHELL:
run-celery:
	 cd src && celery -A celery_app  worker --concurrency=5 -B -E -l INFO


qa: black flake8 mypy

help:
	@echo "Usage:"
	@echo "  make venv - create virtual environment for the project"
	@echo "  make flake8 - run flake8 on the project"
	@echo "  make black - run black on the project"
	@echo "  make mypy - run mypy on the project"
	@echo "  make test-app - run automated tests"
	@echo "  make test-coverage - run automated tests & get test converge statistics"
	@echo "  make qa - run black, mypy and flake8"
	@echo "  make run-app - run server only"
	@echo "  make migrate-up - runs all migrations against the database"
	@echo "  make migrate-down - drops one migration at time"
	@echo "  make docker-pull-db - pulls a Postgres DB docker image"
	@echo "  make docker-run-db - runs the Postgres DB docker image (only first time)"
	@echo "  make docker-stop-db - stops the Postgres DB docker container"
	@echo "  make docker-start-db - starts the Postgres DB docker container"
	@echo "  make docker-delete-db - deletes the Postgres DB docker container"
