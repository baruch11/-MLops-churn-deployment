PROJECT_NAME := chaos
UNIT_TEST_DIR := chaos/test/unit
COV_REPORT_TXT := coverage/coverage.txt
COV_CONFIG_FILE_LOC := coverage/.coveragerc

coverage-unit:
	@pytest --cov=$(PROJECT_NAME) $(UNIT_TEST_DIR) --cov-report=html --cov-config=$(COV_CONFIG_FILE_LOC) --cov-report term > $(COV_REPORT_TXT)

