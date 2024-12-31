all: build run logs

build:
	docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec discord-bot /bin/bash

.PHONY: build run stop logs shell