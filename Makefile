PROJECT_NAME := chaos
UNIT_TEST_DIR := chaos/test/unit
COV_REPORT_TXT := coverage/coverage.txt
COV_CONFIG_FILE_LOC := coverage/.coveragerc
INSTANCE_CONNECTION_NAME := coyotta-2022:europe-west1:ml-prod-coyotta-2022-group-1-sql-16760197
SHORT_SHA := $(shell git rev-parse --short=8 HEAD)


coverage-unit:
	@pytest --cov=$(PROJECT_NAME) $(UNIT_TEST_DIR) --cov-report=html --cov-config=$(COV_CONFIG_FILE_LOC) --cov-report term > $(COV_REPORT_TXT)

run-server:
	uvicorn chaos.application.server:app --host "0.0.0.0" --port 8000

build-docker-image:
	DOCKER_BUILDKIT=1 docker build --platform linux/amd64 \
		--ssh churn_ssh=$(SSH_PRIVATE_KEY) -t eu.gcr.io/coyotta-2022/chaos-1:$(SHORT_SHA) .

run-docker-image:
	docker run -p 8000:8000 -e PORT=8000 -e K_SERVICE=dev \
	-e K_CONFIGURATION=dev -e K_REVISION=dev-00001 \
	-e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/gcp_key.json \
	-v $(GOOGLE_APPLICATION_CREDENTIALS):/tmp/keys/gcp_key.json:ro \
	chaos-1:$(SHORT_SHA)


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


