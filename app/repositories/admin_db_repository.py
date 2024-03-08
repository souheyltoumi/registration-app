
import asyncpg
from datetime import datetime, timedelta
from utils.common import CustomHTTPException

class AdminDBRepository:
    _ERR_PREFIX = "[atrium.AdminDBRepository]"

    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def transaction(self, start : bool = True) -> asyncpg.transaction.Transaction:
        t = self.db.transaction()
        if start:
            await t.start()
        return t

    async def insert_user(self, account: dict) -> int:
        """
        Insert a new user into the users table.
        """
        user_id = await self.db.fetchval(
            "INSERT INTO users (email, password, token_id, active) VALUES ($1, $2, $3, $4) RETURNING id",
            account['email'],
            account['password'],
            account['token_id'],
            False
        )
        return user_id

    async def insert_token(self, token: str) -> int:
        """
        Insert a new token into the tokens table.
        """
        token_id = await self.db.fetchval(
            "INSERT INTO tokens (token, creation_timestamp) VALUES ($1, $2) RETURNING id",
            token,
            datetime.now()
        )
        return token_id

    async def check_account_existance(self, email: str) -> bool:
        """
        check if user email already exists
        """
        user_exist = await self.db.fetchval(
            "SELECT EXISTS(SELECT 1 FROM users WHERE UPPER(email) = $1 )", email.upper()
        )
        return user_exist

    async def account_authenticate(self, email: str, password: str) -> int:
        """
        authenticate user
        """
        user = await self.db.fetchrow(
            "SELECT id, active FROM users WHERE UPPER(email) = $1 AND password = $2", email.upper(), password
        )
        if not user:
            raise CustomHTTPException(
                detail="[account_authenticate] invalid user email or password",
                status_code=409
            )
        if user.get('active'):
            raise CustomHTTPException(
                detail=f"[account_authenticate] account '{email}' already activated",
                status_code=409
            )

        return user.get('id')

    async def validate_account_token(self, account_id: int, supplied_token: str):
        """
        method to validate account token
        """
        token = await self.db.fetchrow(
            """SELECT token, creation_timestamp FROM tokens tk
                JOIN users u ON u.token_id = tk.id
             WHERE u.id = $1 AND tk.token = $2
            """, account_id, supplied_token
        )

        if not token:
            raise CustomHTTPException(
                detail="[validate_account_token] invalid token for account",
                status_code=409
            )

        if datetime.now() - token.get('creation_timestamp') > timedelta(minutes=5):
            raise CustomHTTPException(
                detail="[validate_account_token] expired token",
                status_code=409
            )

    async def activate_user_account(self, account_id):
        """
        method to activate account
        """
        await self.db.execute(
            "UPDATE users SET active = TRUE WHERE id = $1", account_id
        )

    async def refresh_token(self, account_id: int, token: str):
        """
        method to refresh token
        """
        token_id = await self.insert_token(token)

        await self.db.execute(
            "UPDATE users SET token_id = $1 WHERE id = $2", token_id, account_id
        )
