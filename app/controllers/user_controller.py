from strategies import (
    UserAccountActivationRequest,
    UserAccountRegistrationRequest,
    UserAccountRegistrationResponse,
    UserAccountActivationResponse,
    UserAccountRefreshRequest,
    UserAccountRefreshResponse
)

from contexts.user_context import UserContext
import asyncpg

class UserController:

    async def user_account_registration(self, user: UserAccountRegistrationRequest, db: asyncpg.Connection) -> dict:
        return await UserContext(db).registration(user=user)

    async def user_account_activation(self, user: UserAccountActivationRequest, db: asyncpg.Connection) -> dict:
        return await UserContext(db).activate(user=user)

    async def user_account_refresh(self, user: UserAccountActivationRequest, db: asyncpg.Connection) -> dict:
        return await UserContext(db).refresh(user=user)