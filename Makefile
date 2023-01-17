PROJECT_NAME := chaos
UNIT_TEST_DIR := chaos/test/unit
COV_REPORT_TXT := coverage/coverage.txt
COV_CONFIG_FILE_LOC := coverage/.coveragerc
INSTANCE_CONNECTION_NAME := coyotta-2022:europe-west1:ml-prod-coyotta-2022-group-1-sql-16760197
SHORT_SHA := $(shell git rev-parse --short=8 HEAD)


coverage-unit:
	pytest --cov=chaos.domain --cov=chaos.infrastructure --cov=chaos.application  $(UNIT_TEST_DIR) \
		--cov-report=html --cov-config=$(COV_CONFIG_FILE_LOC) --cov-report term > $(COV_REPORT_TXT)

run-server:
	uvicorn chaos.application.server:app --host "0.0.0.0" --port 8000

build-docker-image:
	export SHORT_SHA=$(SHORT_SHA); \
	DOCKER_BUILDKIT=1 docker compose build --ssh churn_ssh=$(SSH_PRIVATE_KEY)

containerize-and-start-app : ## We are exporting the SHORT_SHA to use it in the compose file. 
	export SHORT_SHA=$(SHORT_SHA); \
	DOCKER_BUILDKIT=1 docker compose build --ssh churn_ssh=$(SSH_PRIVATE_KEY); \
	docker compose up

containerize-and-start-bdd:
	export SHORT_SHA=$(SHORT_SHA); \
	docker compose run --service-ports db

containerize-and-run-tests:
	export SHORT_SHA=$(SHORT_SHA); \
	DOCKER_BUILDKIT=1 docker compose build --ssh churn_ssh=$(SSH_PRIVATE_KEY); \
	docker compose run api pytest --cov=chaos.domain --cov=chaos.infrastructure \
		--cov=chaos.application $(UNIT_TEST_DIR) --cov-report=html --cov-config=$(COV_CONFIG_FILE_LOC) --cov-report term 
	docker compose down

proxy-start:
	cloud_sql_proxy -instances=$(INSTANCE_CONNECTION_NAME)=tcp:5432

proxy-kill:
	$(eval PROCESS_ID := $(shell pgrep -f cloud_sql_proxy))		
	@if [  -z "$(PROCESS_ID)" ]; then \
		echo "No running process"; \
	else \
		echo "Running Process ID : $(PROCESS_ID)"; \
		kill $(PROCESS_ID); \
		echo "Running SQL Proxy client has been killed"; \
	fi

postgres-connexion:
	@psql "host=localhost port=5432 sslmode=disable dbname=churnapi \
					 user=coyotta-2022-group-1"


run-perf-tests:
	pytest chaos/test/unit -o python_functions='perf_'
