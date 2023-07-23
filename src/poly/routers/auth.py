from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from poly.config import Settings, get_settings
from poly.db import get_session
from poly.db.schema import Token
from poly.services.auth import authenticate, generate_token

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    user = await authenticate(
        email=form_data.username, password=form_data.password, session=session
    )
    access_token = generate_token(
        user=user, expires_in=settings.access_token_expiry, settings=settings
    )
    refresh_token = generate_token(
        user=user, expires_in=settings.refresh_token_expiry, settings=settings
    )
    response.set_cookie(key="poly_refresh_token", value=refresh_token)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": settings.access_token_expiry * 60,
    }
