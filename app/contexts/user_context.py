import asyncpg
from strategies import (
    UserAccountActivationRequest,
    UserAccountRegistrationRequest,
    UserAccountRegistrationResponse,
    UserAccountActivationResponse,
    UserAccountRefreshRequest,
    UserAccountRefreshResponse
)

from repositories.admin_db_repository import AdminDBRepository
from utils.common import generate_4_digit_code, AppLogger, CustomHTTPException
from utils.mailer import send_mail, MailTemplates

class UserContext:

    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def registration(self, user: UserAccountRegistrationRequest) -> dict:
        """
        context method to register new user account
        """
        admin_repository = AdminDBRepository(self.db)
        admin_repository_transaction = await admin_repository.transaction()
        try:

            if (await admin_repository.check_account_existance(user.email)):
                raise CustomHTTPException(
                    detail=f"[check_account_existance] user with email '{user.email}' already registred",
                    status_code=409
                )

            user_code = generate_4_digit_code()
            token_id = await admin_repository.insert_token(user_code)
            user_id = await admin_repository.insert_user(
                account={
                    **user.dict(),
                    'token_id': token_id
                }
            )

            AppLogger.log(f"[insert_token] user is registred successfly in db with id #{user_id}")
            send_mail(
                user.email,
                MailTemplates['account_activation_token'].value(activation_code=user_code),
                'Account activation token'  
            )
            response = UserAccountRegistrationResponse(message=f"[success] user successfly registred and an email was sent to '{user.email}'")
            await admin_repository_transaction.commit()

        except Exception as ex:
            AppLogger.log(f"[exception]: {str(ex)}")
            await admin_repository_transaction.rollback()
            raise ex
        return response.dict()

    async def refresh(self, user: UserAccountRefreshRequest) -> dict:
        """
        context method to refresh token
        """
        admin_repository = AdminDBRepository(self.db)
        admin_repository_transaction = await admin_repository.transaction()
        try:
            account_id = await admin_repository.account_authenticate(user.email, user.password)
            new_user_code = generate_4_digit_code()
            await admin_repository.refresh_token(account_id, new_user_code)
            send_mail(
                user.email,
                MailTemplates['account_refresh_token'].value(new_activation_code=new_user_code),
                'Account activation token'  
            )
            await admin_repository_transaction.commit()
            response = UserAccountRefreshResponse(message=f"[success] token refreshed successfly and an email was sent to '{user.email}'")
        except Exception as ex:
            AppLogger.log(f"[exception]: {str(ex)}")
            await admin_repository_transaction.rollback()
            raise ex
        return response.dict()

    async def activate(self, user: UserAccountActivationRequest) -> dict:
        """
        context method to activate a user account using activation token
        """
        admin_repository = AdminDBRepository(self.db)
        admin_repository_transaction = await admin_repository.transaction()
        try:
            account_id = await admin_repository.account_authenticate(user.email, user.password)
            await admin_repository.validate_account_token(account_id, user.token)
            await admin_repository.activate_user_account(account_id)
            send_mail(
                user.email,
                MailTemplates['account_activated_mail'].value,
                'Account activated successfuly'  
            )
            response = UserAccountRegistrationResponse(message=f"[success] user account successfly activated '{user.email}'")
            await admin_repository_transaction.commit()
        except Exception as ex:
            AppLogger.log(f"[exception]: {str(ex)}")
            await admin_repository_transaction.rollback()
            raise ex
        return response.dict()
