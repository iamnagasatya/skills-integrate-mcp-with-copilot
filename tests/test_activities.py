import os
import sys
import pytest
# Ensure project root is on PYTHONPATH for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert "Chess Club" in resp.json()


def test_signup_success():
    resp = client.post("/activities/Chess Club/signup", json={"email": "test@example.com"})
    assert resp.status_code == 200
    assert "Signed up test@example.com" in resp.json()["message"]
    # cleanup
    client.request("DELETE", "/activities/Chess Club/unregister", json={"email": "test@example.com"})


def test_signup_invalid_email():
    resp = client.post("/activities/Chess Club/signup", json={"email": "not-an-email"})
    assert resp.status_code == 422


def test_signup_duplicate():
    # Try to sign up existing participant in activities dict
    resp = client.post("/activities/Chess Club/signup", json={"email": "michael@mergington.edu"})
    assert resp.status_code == 400


def test_unregister_not_signed_up():
    resp = client.request("DELETE", "/activities/Chess Club/unregister", json={"email": "noone@example.com"})
    assert resp.status_code == 400


def test_unregister_success():
    client.post("/activities/Chess Club/signup", json={"email": "temp@example.com"})
    resp = client.request("DELETE", "/activities/Chess Club/unregister", json={"email": "temp@example.com"})
    assert resp.status_code == 200
