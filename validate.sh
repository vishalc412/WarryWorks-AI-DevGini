#!/bin/bash

# Validation script to check if the platform is working correctly

set -e

echo "=========================================="
echo "Lovable-AI Builder Platform Validation"
echo "=========================================="
echo ""

# Check if services are running
echo "Checking if services are running..."
if docker-compose ps | grep -q "Up"; then
    echo "✓ Docker services are running"
else
    echo "✗ Docker services are not running"
    echo "  Run: docker-compose up -d"
    exit 1
fi

echo ""
echo "Checking backend health..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✓ Backend is healthy"
else
    echo "✗ Backend is not responding"
    exit 1
fi

echo ""
echo "Checking frontend..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Frontend is accessible"
else
    echo "✗ Frontend is not accessible"
    exit 1
fi

echo ""
echo "Checking API documentation..."
if curl -s http://localhost:8000/api/docs > /dev/null 2>&1; then
    echo "✓ API docs are accessible"
else
    echo "✗ API docs are not accessible"
    exit 1
fi

echo ""
echo "=========================================="
echo "Validation Complete - All checks passed!"
echo "=========================================="
echo ""
echo "You can now use the platform:"
echo "  • Open http://localhost:3000 to get started"
echo ""
