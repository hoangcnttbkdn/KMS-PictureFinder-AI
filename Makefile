ifneq ("$(wildcard .env)","")
	include .env
	export
endif

install:
	pip install -r requirements.txt

run:
	cd src && uvicorn app:app --port ${PORT}