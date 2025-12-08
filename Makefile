# Makefile for Payouts Service

PYTHON=python
MANAGE=$(PYTHON) payouts_project/manage.py

# Local Django Commands

run:
	$(MANAGE) runserver

test:
	cd payouts_project && \
	$(PYTHON) manage.py test -v 2

worker:
	# On Linux:   celery -A payouts_project worker -l info --concurrency=4
	# On Windows: celery -A payouts_project worker -l info -P solo
	cd payouts_project && \
	celery -A payouts_project worker -l info --concurrency=4

pip:
	pip install -r payouts_project/requirements.txt

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

collectstatic:
	$(MANAGE) collectstatic --noinput

# Docker Compose Commands

up_services:
	docker compose -f docker-compose.services.yml up -d

down_services:
	docker compose -f docker-compose.services.yml down

logs_services:
	docker compose -f docker-compose.services.yml logs -f

# Production
up_prod:
	docker compose -f docker-compose.prod.yml up --build

down_prod:
	docker compose -f docker-compose.prod.yml down

logs_prod:
	docker compose -f docker-compose.prod.yml logs -f

# Utilities

shell:
	$(MANAGE) shell

superuser:
	$(MANAGE) createsuperuser

reset_db:
	$(MANAGE) flush --noinput
