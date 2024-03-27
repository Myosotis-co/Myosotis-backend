from typing import Optional
from app.email.router import simple_send
from app.email.schema import EmailSchema
from pydantic import BaseModel
from fastapi import Depends, Request, status
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from app.auth.functions import get_user_db
from app.auth.models import User
from fastapi.responses import JSONResponse

from typing import List

SECRET = "verysecuresecretpisdec"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    UserManager class for managing user creation, authentication, and authorization.
    Inherits from IntegerIDMixin and BaseUserManager.
    """

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):

        print(f"Trying to send verification code...")
        try:
            email_instance = EmailSchema(email=[user.email])
            await simple_send(email_instance, token)
        except Exception as e:
            print(f"Failed to send message {user.email}: {e}")
        
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has been verified")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Method for creating a new user.
        :param user_create: UserCreate object representing the user to be created.
        :param safe: Optional boolean indicating whether to create a safe user or a superuser.
        :param request: Optional Request object representing the HTTP request.
        :return: User object representing the created user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 2
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user

    async def oauth_callback(
        self: "BaseUserManager[models.UOAP, models.ID]",
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[int] = None,
        refresh_token: Optional[str] = None,
        request: Optional[Request] = None,
        *,
        associate_by_email: bool = False,
    ) -> models.UOAP:
        """
        Method for handling OAuth callbacks and registering or authenticating users.
        :param oauth_name: String representing the name of the OAuth provider.
        :param access_token: String representing the access token returned by the OAuth provider.
        :param account_id: String representing the ID of the account returned by the OAuth provider.
        :param account_email: String representing the email of the account returned by the OAuth provider.
        :param expires_at: Optional integer representing the expiration time of the access token.
        :param refresh_token: Optional string representing the refresh token returned by the OAuth provider.
        :param request: Optional Request object representing the HTTP request.
        :param associate_by_email: Optional boolean indicating whether to associate the OAuth account with an existing user
        based on email.
        :return: UserOAuthAccount object representing the user's OAuth account.
        """
        
        oauth_account_dict = {
            "oauth_name": oauth_name,
            "access_token": access_token,
            "account_id": account_id,
            "account_email": account_email,
            "expires_at": expires_at,
            "refresh_token": refresh_token,
        }

        try:
            user = await self.get_by_oauth_account(oauth_name, account_id)
        except exceptions.UserNotExists:
            try:
                # Associate account
                user = await self.get_by_email(account_email)
                if not associate_by_email:
                    raise exceptions.UserAlreadyExists()
                user = await self.user_db.add_oauth_account(user, oauth_account_dict)
            except exceptions.UserNotExists:
                # Create account
                password = self.password_helper.generate()
                user_dict = {
                    "email": account_email,
                    "role_id": 2,
                    "name": account_email,
                    "hashed_password": self.password_helper.hash(password),
                }
                user = await self.user_db.create(user_dict)
                user = await self.user_db.add_oauth_account(user, oauth_account_dict)
                await self.on_after_register(user, request)
        else:
            # Update oauth
            for existing_oauth_account in user.oauth_accounts:
                if (
                    existing_oauth_account.account_id == account_id
                    and existing_oauth_account.oauth_name == oauth_name
                ):
                    user = await self.user_db.update_oauth_account(
                        user, existing_oauth_account, oauth_account_dict
                    )

        return user


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Returns an instance of UserManager class with the provided user_db as a dependency.

    Args:
        user_db: The user database.

    Returns:
        An instance of UserManager class.
    """
    yield UserManager(user_db)
