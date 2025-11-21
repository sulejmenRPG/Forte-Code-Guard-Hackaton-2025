"""
Tests for webhook functionality
"""

import pytest
from fastapi.testclient import TestClient
import sys
sys.path.append('../backend')

from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Code Review" in response.json()["message"]


def test_webhook_without_token():
    """Test webhook without authentication"""
    response = client.post("/webhook/gitlab", json={})
    assert response.status_code == 401


def test_webhook_with_wrong_event():
    """Test webhook with non-MR event"""
    payload = {
        "object_kind": "push",
        "object_attributes": {}
    }
    response = client.post(
        "/webhook/gitlab",
        json=payload,
        headers={"X-Gitlab-Token": "test_secret"}
    )
    # Should be ignored
    assert response.status_code in [200, 401]
