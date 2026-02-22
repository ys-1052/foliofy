from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


# Request/Response Models
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpResponse(BaseModel):
    user_sub: str
    user_confirmed: bool
    message: str


class ConfirmSignUpRequest(BaseModel):
    email: EmailStr
    confirmation_code: str


class ConfirmSignUpResponse(BaseModel):
    confirmed: bool
    message: str


class ResendCodeRequest(BaseModel):
    email: EmailStr


class ResendCodeResponse(BaseModel):
    message: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignInResponse(BaseModel):
    id_token: str
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    id_token: str
    access_token: str
    expires_in: int
    token_type: str


class SignOutRequest(BaseModel):
    access_token: str


class SignOutResponse(BaseModel):
    signed_out: bool
    message: str


# Endpoints
@router.post("/signup", response_model=SignUpResponse, status_code=status.HTTP_201_CREATED)
def sign_up(request: SignUpRequest):
    """Sign up a new user"""
    try:
        result = auth_service.sign_up(email=request.email, password=request.password)
        return SignUpResponse(
            user_sub=result["user_sub"],
            user_confirmed=result["user_confirmed"],
            message=(
                "Sign up complete. Please enter the verification code sent to your email."
                if not result["user_confirmed"]
                else "Sign up complete."
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/confirm", response_model=ConfirmSignUpResponse)
def confirm_sign_up(request: ConfirmSignUpRequest):
    """Confirm email verification"""
    try:
        auth_service.confirm_sign_up(
            email=request.email, confirmation_code=request.confirmation_code
        )
        return ConfirmSignUpResponse(confirmed=True, message="Email address confirmed.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/resend-code", response_model=ResendCodeResponse)
def resend_confirmation_code(request: ResendCodeRequest):
    """Resend verification code"""
    try:
        auth_service.resend_confirmation_code(email=request.email)
        return ResendCodeResponse(message="Verification code resent.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/signin", response_model=SignInResponse)
def sign_in(request: SignInRequest):
    """Sign in"""
    try:
        result = auth_service.sign_in(email=request.email, password=request.password)
        return SignInResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(request: RefreshTokenRequest):
    """Refresh access token"""
    try:
        result = auth_service.refresh_token(refresh_token=request.refresh_token)
        return RefreshTokenResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.post("/signout", response_model=SignOutResponse)
def sign_out(request: SignOutRequest):
    """Sign out"""
    try:
        auth_service.sign_out(access_token=request.access_token)
        return SignOutResponse(signed_out=True, message="Signed out successfully.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e
