.DEFAULT_GOAL := default

run_api:
	uvicorn project_walmart.api.fast:app --reload
