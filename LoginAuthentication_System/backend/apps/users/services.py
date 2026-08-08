from django.db import transaction
from apps.users.models import User
from apps.users.schemas import UserRegisterSchema
from apps.users.tokens import generate_email_token, verify_email_token
from core.exceptions import BaseAppException, NotFoundError

class UserService:
    @staticmethod
    @transaction.atomic
    def register_user(data: UserRegisterSchema) -> User:
        email = data.email.lower()
        if User.objects.filter(email=email).exists():
            raise BaseAppException(message="User with this email already exists.", status_code=409)
        
        user = User.objects.create_user(
            email=email,
            password=data.password,
            first_name=data.first_name or "",
            last_name=data.last_name or ""
        )
        return user

    @staticmethod
    def get_verification_token(user: User) -> str:
        return generate_email_token(str(user.id))

    @staticmethod
    def verify_email(token: str) -> bool:
        user_id = verify_email_token(token)
        if not user_id:
            raise BaseAppException(message="Invalid or expired verification token.", status_code=400)
        
        try:
            user = User.objects.get(id=user_id)
            user.is_email_verified = True
            user.save(update_fields=["is_email_verified"])
            return True
        except User.DoesNotExist:
            raise NotFoundError("User not found.")
