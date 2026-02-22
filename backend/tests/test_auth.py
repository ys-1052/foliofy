"""Tests for authentication endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError


def test_signup_success(client):
    """Test successful user signup."""
    with patch("app.services.auth_service.auth_service.sign_up") as mock_signup:
        mock_signup.return_value = {
            "user_sub": "test-sub-123",
            "user_confirmed": False,
            "code_delivery_details": {"Destination": "t***@example.com"},
        }

        response = client.post(
            "/auth/signup",
            json={"email": "test@example.com", "password": "Test1234"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["user_sub"] == "test-sub-123"
        assert data["user_confirmed"] is False
        assert "verification code" in data["message"]


def test_signup_duplicate_email(client):
    """Test signup with existing email."""
    with patch("app.services.auth_service.auth_service.sign_up") as mock_signup:
        mock_signup.side_effect = ValueError("This email address is already registered")

        response = client.post(
            "/auth/signup",
            json={"email": "existing@example.com", "password": "Test1234"},
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]


def test_confirm_signup_success(client):
    """Test successful email confirmation."""
    with patch(
        "app.services.auth_service.auth_service.confirm_sign_up"
    ) as mock_confirm:
        mock_confirm.return_value = {"confirmed": True}

        response = client.post(
            "/auth/confirm",
            json={"email": "test@example.com", "confirmation_code": "123456"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["confirmed"] is True
        assert "confirmed" in data["message"].lower()


def test_confirm_signup_invalid_code(client):
    """Test email confirmation with invalid code."""
    with patch(
        "app.services.auth_service.auth_service.confirm_sign_up"
    ) as mock_confirm:
        mock_confirm.side_effect = ValueError("Invalid verification code")

        response = client.post(
            "/auth/confirm",
            json={"email": "test@example.com", "confirmation_code": "wrong"},
        )

        assert response.status_code == 400
        assert "Invalid verification code" in response.json()["detail"]


def test_resend_code_success(client):
    """Test resending confirmation code."""
    with patch(
        "app.services.auth_service.auth_service.resend_confirmation_code"
    ) as mock_resend:
        mock_resend.return_value = {
            "code_delivery_details": {"Destination": "t***@example.com"}
        }

        response = client.post(
            "/auth/resend-code",
            json={"email": "test@example.com"},
        )

        assert response.status_code == 200
        assert "resent" in response.json()["message"].lower()


def test_signin_success(client):
    """Test successful signin."""
    with patch("app.services.auth_service.auth_service.sign_in") as mock_signin:
        mock_signin.return_value = {
            "id_token": "test-id-token",
            "access_token": "test-access-token",
            "refresh_token": "test-refresh-token",
            "expires_in": 3600,
            "token_type": "Bearer",
        }

        response = client.post(
            "/auth/signin",
            json={"email": "test@example.com", "password": "Test1234"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id_token"] == "test-id-token"
        assert data["access_token"] == "test-access-token"
        assert data["token_type"] == "Bearer"


def test_signin_invalid_credentials(client):
    """Test signin with invalid credentials."""
    with patch("app.services.auth_service.auth_service.sign_in") as mock_signin:
        mock_signin.side_effect = ValueError("Incorrect email or password")

        response = client.post(
            "/auth/signin",
            json={"email": "test@example.com", "password": "wrong"},
        )

        assert response.status_code == 401
        assert "Incorrect" in response.json()["detail"]


def test_signin_user_not_confirmed(client):
    """Test signin with unconfirmed user."""
    with patch("app.services.auth_service.auth_service.sign_in") as mock_signin:
        mock_signin.side_effect = ValueError("Email address not confirmed")

        response = client.post(
            "/auth/signin",
            json={"email": "test@example.com", "password": "Test1234"},
        )

        assert response.status_code == 401
        assert "not confirmed" in response.json()["detail"]


def test_refresh_token_success(client):
    """Test token refresh."""
    with patch(
        "app.services.auth_service.auth_service.refresh_token"
    ) as mock_refresh:
        mock_refresh.return_value = {
            "id_token": "new-id-token",
            "access_token": "new-access-token",
            "expires_in": 3600,
            "token_type": "Bearer",
        }

        response = client.post(
            "/auth/refresh",
            json={"refresh_token": "test-refresh-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id_token"] == "new-id-token"
        assert data["access_token"] == "new-access-token"


def test_signout_success(client):
    """Test signout."""
    with patch("app.services.auth_service.auth_service.sign_out") as mock_signout:
        mock_signout.return_value = {"signed_out": True}

        response = client.post(
            "/auth/signout",
            json={"access_token": "test-access-token"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["signed_out"] is True
        assert "Signed out" in data["message"]
