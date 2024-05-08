.DEFAULT_GOAL := default

run_api:
	uvicorn walmart.api.fast:app --reload
