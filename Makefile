docker_file ?= -f docker-compose.yml
exec_flag ?=

createsuperuser:
	docker-compose $(docker_file) exec $(exec_flag) web python manage.py createsuperuser

makemigrations:
	docker-compose $(docker_file) exec $(exec_flag) web python manage.py makemigrations

migrate:
	docker-compose $(docker_file) exec $(exec_flag) web python manage.py migrate

install-package:
	pip install -r requirements/base.txt

flush-db:
	docker-compose $(docker_file) exec $(exec_flag) web python manage.py flush

sample-data:
	docker-compose $(docker_file) exec $(exec_flag) web python manage.py setup_test_data

run-test:
	docker-compose $(docker_file) exec $(exec_flag) web python manage.py test