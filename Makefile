.PHONY: help setup up down logs clean test backend-test frontend-test validate

help:
	@echo "Lovable-AI Builder Platform - Available Commands"
	@echo ""
	@echo "Setup & Running:"
	@echo "  make setup          - Initial setup with environment files"
	@echo "  make up             - Start all services with Docker Compose"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View logs from all services"
	@echo "  make validate       - Validate platform is working"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run all tests"
	@echo "  make backend-test   - Run backend tests only"
	@echo "  make frontend-test  - Run frontend tests only"
	@echo ""
	@echo "Development:"
	@echo "  make clean          - Clean up generated files and containers"
	@echo ""

setup:
	@echo "Setting up environment files..."
	@cp -n .env.example .env || echo ".env already exists"
	@cp -n frontend/.env.example frontend/.env || echo "frontend/.env already exists"
	@echo "✓ Setup complete. Remember to add your API keys to .env"

up:
	@echo "Starting services..."
	@docker-compose up -d
	@echo "✓ Services started"
	@echo "  Frontend: http://localhost:3000"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/api/docs"

down:
	@echo "Stopping services..."
	@docker-compose down
	@echo "✓ Services stopped"

logs:
	@docker-compose logs -f

validate:
	@bash validate.sh

test: backend-test frontend-test

backend-test:
	@echo "Running backend tests..."
	@cd backend && pytest

frontend-test:
	@echo "Running frontend tests..."
	@cd frontend && npm test --passWithNoTests

clean:
	@echo "Cleaning up..."
	@docker-compose down -v
	@rm -rf backend/__pycache__ backend/.pytest_cache backend/htmlcov
	@rm -rf frontend/node_modules frontend/dist
	@echo "✓ Cleaned up"
