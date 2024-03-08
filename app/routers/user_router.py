from fastapi import APIRouter, Request, Depends, Query
from strategies import (
    UserAccountActivationRequest,
    UserAccountRegistrationRequest,
    UserAccountRegistrationResponse,
    UserAccountActivationResponse,
    UserAccountRefreshRequest,
    UserAccountRefreshResponse
)

from dao.conf.dao_base import admin_dbh
import asyncpg

from routers.dispatcher import get_controller
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from utils.common import CustomHTTPException

router = APIRouter(
    tags=["User Account"],
)

security = HTTPBasic()

@router.post("/users/register", summary="Register user account", response_model=UserAccountRegistrationResponse)
async def register_account(user: UserAccountRegistrationRequest, request: Request, db: asyncpg.Connection = Depends(admin_dbh), controller=Depends(get_controller)):
    registration_response = await controller.user_account_registration(user, db)
    return registration_response

@router.post("/users/activation", summary="Activate user account", response_model=UserAccountActivationResponse)
async def activate_account(
    request: Request,
    token: str = Query(description="account activation token", min_length=4, max_length=4, regex=r'\d{4}', default="4910"),
    db: asyncpg.Connection = Depends(admin_dbh),
    controller=Depends(get_controller), 
    credentials: HTTPBasicCredentials = Depends(security)
    ):
    user = UserAccountActivationRequest(
        email= credentials.username,
        password = credentials.password,
        token=token
    )
    activation_response = await controller.user_account_activation(user, db)
    return activation_response

@router.post("/users/refresh", summary="Refresh user account token", response_model=UserAccountRefreshResponse)
async def refresh_token(
    request: Request,
    db: asyncpg.Connection = Depends(admin_dbh),
    controller=Depends(get_controller), 
    credentials: HTTPBasicCredentials = Depends(security)
    ):
    user = UserAccountRefreshRequest(
        email= credentials.username,
        password = credentials.password,
    )
    refresh_response = await controller.user_account_refresh(user, db)
    return refresh_response