PROJECT_NAME := chaos
UNIT_TEST_DIR := chaos/test/unit


coverage-unit:
	@pytest --cov=$(PROJECT_NAME) $(UNIT_TEST_DIR) --cov-report=html

