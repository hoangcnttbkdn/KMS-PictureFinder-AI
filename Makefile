ifneq ("$(wildcard .env)","")
	include .env
	export
endif

install:
	pip install -r requirements.txt

run:
	uvicorn src.app:app --port ${PORT}

dc-up:
	docker compose up -d