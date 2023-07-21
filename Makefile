# Makefile generated with pymakefile
help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

migrations:
	docker-compose run --rm api python3 manage.py makemigrations

migrate:
	docker-compose run --rm api python3 manage.py migrate

lint:
	docker-compose run --rm api make check

check:  ## Fix code to pep8 standards
	black .
	isort . --profile black
	flake8 .

superuser: # Create django superuser
	docker-compose run --rm api python3 manage.py createsuperuser

run:
	docker-compose run --rm -p 8000:8000 api

runtests:
	docker-compose run --rm api pytest --reuse-db --create-db --no-migrations

shell:
	docker-compose run --rm api python3 manage.py shell

apikey:
	docker-compose run -T --rm api python3 manage.py shell < ./scripts/apikey.py
