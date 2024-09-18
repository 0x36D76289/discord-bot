DOCKER-COMPOSE = docker-compose

all: build up

build:
	$(DOCKER-COMPOSE) build

up:
	$(DOCKER-COMPOSE) up -d

down:
	$(DOCKER-COMPOSE) down

logs:
	$(DOCKER-COMPOSE) logs -f

.PHONY: all build up down logs
