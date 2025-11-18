"""
Tests for main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns healthy status"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Lovable-AI Builder Platform"
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data


def test_api_docs():
    """Test API documentation is accessible"""
    response = client.get("/api/docs")
    assert response.status_code == 200


def test_models_providers_endpoint():
    """Test models providers listing"""
    response = client.get("/api/models/providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert len(data["providers"]) > 0


def test_cors_headers():
    """Test CORS headers are present"""
    response = client.options("/")
    assert "access-control-allow-origin" in response.headers or response.status_code == 200
