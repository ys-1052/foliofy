import base64
import hashlib
import hmac

import boto3
import requests  # type: ignore[import-untyped]
from botocore.exceptions import ClientError
from jose import JWTError, jwt

from app.config import settings


class AuthService:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=settings.aws_region)
        self.user_pool_id = settings.cognito_user_pool_id
        self.client_id = settings.cognito_client_id
        self._jwks = None

    def _get_secret_hash(self, username: str) -> str:
        """
        Generate hash for Cognito Client Secret.
        Currently unused since generateSecret=false, kept for future use.
        """
        message = bytes(username + self.client_id, "utf-8")
        secret = bytes("", "utf-8")  # No Client Secret
        dig = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def sign_up(self, email: str, password: str) -> dict:
        """Sign up a new user"""
        try:
            response = self.client.sign_up(
                ClientId=self.client_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                ],
            )
            return {
                "user_sub": response["UserSub"],
                "user_confirmed": response["UserConfirmed"],
                "code_delivery_details": response.get("CodeDeliveryDetails"),
            }
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "UsernameExistsException":
                raise ValueError("This email address is already registered") from e
            elif error_code == "InvalidPasswordException":
                raise ValueError("Password does not meet requirements") from e
            elif error_code == "InvalidParameterException":
                raise ValueError("Invalid input parameter") from e
            else:
                raise Exception(f"Sign up error: {e.response['Error']['Message']}") from e

    def confirm_sign_up(self, email: str, confirmation_code: str) -> dict:
        """Confirm sign up with email verification code"""
        try:
            self.client.confirm_sign_up(
                ClientId=self.client_id,
                Username=email,
                ConfirmationCode=confirmation_code,
            )
            return {"confirmed": True}
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "CodeMismatchException":
                raise ValueError("Invalid verification code") from e
            elif error_code == "ExpiredCodeException":
                raise ValueError("Verification code has expired") from e
            else:
                raise Exception(f"Verification error: {e.response['Error']['Message']}") from e

    def resend_confirmation_code(self, email: str) -> dict:
        """Resend verification code"""
        try:
            response = self.client.resend_confirmation_code(
                ClientId=self.client_id,
                Username=email,
            )
            return {"code_delivery_details": response.get("CodeDeliveryDetails")}
        except ClientError as e:
            raise Exception(f"Resend error: {e.response['Error']['Message']}") from e

    def sign_in(self, email: str, password: str) -> dict:
        """Sign in"""
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="USER_PASSWORD_AUTH",
                AuthParameters={
                    "USERNAME": email,
                    "PASSWORD": password,
                },
            )

            if "AuthenticationResult" in response:
                auth_result = response["AuthenticationResult"]
                return {
                    "id_token": auth_result["IdToken"],
                    "access_token": auth_result["AccessToken"],
                    "refresh_token": auth_result["RefreshToken"],
                    "expires_in": auth_result["ExpiresIn"],
                    "token_type": auth_result["TokenType"],
                }
            else:
                raise Exception("Authentication failed")

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NotAuthorizedException":
                raise ValueError("Incorrect email or password") from e
            elif error_code == "UserNotConfirmedException":
                raise ValueError("Email address not confirmed") from e
            elif error_code == "UserNotFoundException":
                raise ValueError("User not found") from e
            else:
                raise Exception(f"Sign in error: {e.response['Error']['Message']}") from e

    def refresh_token(self, refresh_token: str) -> dict:
        """Get new access token using refresh token"""
        try:
            response = self.client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={
                    "REFRESH_TOKEN": refresh_token,
                },
            )

            auth_result = response["AuthenticationResult"]
            return {
                "id_token": auth_result["IdToken"],
                "access_token": auth_result["AccessToken"],
                "expires_in": auth_result["ExpiresIn"],
                "token_type": auth_result["TokenType"],
            }
        except ClientError as e:
            raise Exception(f"Token refresh error: {e.response['Error']['Message']}") from e

    def _get_jwks(self) -> dict:
        """Get Cognito public keys (JWKS)"""
        if self._jwks is None:
            keys_url = f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
            response = requests.get(keys_url)
            response.raise_for_status()
            self._jwks = response.json()
        return self._jwks  # type: ignore[no-any-return]

    def verify_token(self, token: str) -> dict:
        """Verify JWT token and return payload"""
        try:
            # Get kid from JWT header
            headers = jwt.get_unverified_header(token)
            kid = headers["kid"]

            # Find public key matching kid from JWKS
            jwks = self._get_jwks()
            key = None
            for jwk in jwks["keys"]:
                if jwk["kid"] == kid:
                    key = jwk
                    break

            if not key:
                raise ValueError("Public key not found")

            # Verify token
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{self.user_pool_id}",
            )

            return payload  # type: ignore[no-any-return]

        except JWTError as e:
            raise ValueError(f"Token verification error: {str(e)}") from e

    def sign_out(self, access_token: str) -> dict:
        """Sign out (global sign out)"""
        try:
            self.client.global_sign_out(AccessToken=access_token)
            return {"signed_out": True}
        except ClientError as e:
            raise Exception(f"Sign out error: {e.response['Error']['Message']}") from e


# Singleton instance
auth_service = AuthService()
