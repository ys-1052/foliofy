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
        Cognito Client Secret用のハッシュを生成
        現在はgenerateSecret=falseなので不要だが、将来用に残す
        """
        message = bytes(username + self.client_id, "utf-8")
        secret = bytes("", "utf-8")  # Client Secretがない場合
        dig = hmac.new(secret, msg=message, digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def sign_up(self, email: str, password: str) -> dict:
        """ユーザー登録"""
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
                raise ValueError("このメールアドレスは既に登録されています") from e
            elif error_code == "InvalidPasswordException":
                raise ValueError("パスワードが要件を満たしていません") from e
            elif error_code == "InvalidParameterException":
                raise ValueError("入力パラメータが無効です") from e
            else:
                raise Exception(f"登録エラー: {e.response['Error']['Message']}") from e

    def confirm_sign_up(self, email: str, confirmation_code: str) -> dict:
        """メール検証コードで登録確認"""
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
                raise ValueError("検証コードが正しくありません") from e
            elif error_code == "ExpiredCodeException":
                raise ValueError("検証コードの有効期限が切れています") from e
            else:
                raise Exception(f"検証エラー: {e.response['Error']['Message']}") from e

    def resend_confirmation_code(self, email: str) -> dict:
        """検証コード再送信"""
        try:
            response = self.client.resend_confirmation_code(
                ClientId=self.client_id,
                Username=email,
            )
            return {"code_delivery_details": response.get("CodeDeliveryDetails")}
        except ClientError as e:
            raise Exception(f"再送信エラー: {e.response['Error']['Message']}") from e

    def sign_in(self, email: str, password: str) -> dict:
        """サインイン"""
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
                raise Exception("認証に失敗しました")

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NotAuthorizedException":
                raise ValueError("メールアドレスまたはパスワードが正しくありません") from e
            elif error_code == "UserNotConfirmedException":
                raise ValueError("メールアドレスが確認されていません") from e
            elif error_code == "UserNotFoundException":
                raise ValueError("ユーザーが見つかりません") from e
            else:
                raise Exception(f"サインインエラー: {e.response['Error']['Message']}") from e

    def refresh_token(self, refresh_token: str) -> dict:
        """リフレッシュトークンで新しいアクセストークンを取得"""
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
            raise Exception(f"トークン更新エラー: {e.response['Error']['Message']}") from e

    def _get_jwks(self) -> dict:
        """Cognito公開鍵（JWKS）を取得"""
        if self._jwks is None:
            keys_url = f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
            response = requests.get(keys_url)
            response.raise_for_status()
            self._jwks = response.json()
        return self._jwks  # type: ignore[no-any-return]

    def verify_token(self, token: str) -> dict:
        """JWTトークンを検証してペイロードを返す"""
        try:
            # JWTヘッダーからkidを取得
            headers = jwt.get_unverified_header(token)
            kid = headers["kid"]

            # JWKS から kid に対応する公開鍵を探す
            jwks = self._get_jwks()
            key = None
            for jwk in jwks["keys"]:
                if jwk["kid"] == kid:
                    key = jwk
                    break

            if not key:
                raise ValueError("公開鍵が見つかりません")

            # トークンを検証
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{self.user_pool_id}",
            )

            return payload  # type: ignore[no-any-return]

        except JWTError as e:
            raise ValueError(f"トークン検証エラー: {str(e)}") from e

    def sign_out(self, access_token: str) -> dict:
        """サインアウト（グローバルサインアウト）"""
        try:
            self.client.global_sign_out(AccessToken=access_token)
            return {"signed_out": True}
        except ClientError as e:
            raise Exception(f"サインアウトエラー: {e.response['Error']['Message']}") from e


# シングルトンインスタンス
auth_service = AuthService()
