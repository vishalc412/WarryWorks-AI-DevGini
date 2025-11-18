#!/bin/bash

# Lovable-AI Builder Platform - Quick Setup Script

set -e

echo "=========================================="
echo "Lovable-AI Builder Platform Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY (optional)"
    echo "   - GOOGLE_API_KEY (optional)"
    echo ""
else
    echo "✓ .env file already exists"
fi

# Check if frontend/.env exists
if [ ! -f frontend/.env ]; then
    echo "Creating frontend/.env file..."
    cp frontend/.env.example frontend/.env
    echo "✓ frontend/.env created"
else
    echo "✓ frontend/.env file already exists"
fi

echo ""
echo "=========================================="
echo "Starting services with Docker Compose..."
echo "=========================================="
echo ""

# Start docker-compose
docker-compose up -d

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Services are now running:"
echo "  • Frontend:  http://localhost:3000"
echo "  • Backend:   http://localhost:8000"
echo "  • API Docs:  http://localhost:8000/api/docs"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
echo "⚠️  Don't forget to add your API keys to .env file!"
echo ""
