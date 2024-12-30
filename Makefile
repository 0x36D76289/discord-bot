# Variables
PROJECT_NAME := discord-bot
ENV_FILE := .env
DOCKER_COMPOSE := docker-compose

# all
all: build run logs

# Help Menu
.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  build         Build the Docker image"
	@echo "  run           Run the bot using Docker Compose"
	@echo "  stop          Stop the bot using Docker Compose"
	@echo "  restart       Restart the bot"
	@echo "  logs          View the bot's logs"
	@echo "  test          Run the tests"
	@echo "  clean         Remove Docker image and containers"
	@echo "  setup         Set up the project (clone, create .env, etc.)"
	@echo "  push          Push the Docker image to a registry (if configured)"
	@echo "  lint          Lint the code using flake8"

# Build the Docker image
.PHONY: build
build:
	@echo "Building Docker image..."
	$(DOCKER_COMPOSE) build

# Run the bot using Docker Compose
.PHONY: run
run:
	@echo "Starting the bot..."
	$(DOCKER_COMPOSE) up -d --build

# Stop the bot using Docker Compose
.PHONY: stop
stop:
	@echo "Stopping the bot..."
	$(DOCKER_COMPOSE) down

# Restart the bot
.PHONY: restart
restart: stop run

# View the bot's logs
.PHONY: logs
logs:
	$(DOCKER_COMPOSE) logs -f $(PROJECT_NAME)

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	docker run --rm -v $(PWD):/app $(PROJECT_NAME) pytest src/tests

# Lint code using flake8
.PHONY: lint
lint:
	@echo "Running linter..."
	docker run --rm -v $(PWD):/app $(PROJECT_NAME) flake8 src

# Clean up Docker image and containers
.PHONY: clean
clean: stop
	@echo "Removing Docker image and containers..."
	docker rmi $(PROJECT_NAME)
	docker rm $$(docker ps -aq -f "name=$(PROJECT_NAME)")

# Set up the project
.PHONY: setup
setup:
	@echo "Setting up the project..."
	@if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); echo "Created .env file. Please configure it."; fi
