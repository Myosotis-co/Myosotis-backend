from app.auth.models import User


def check_user_access(user: User, requested_model):
    if requested_model.user_id != user.id and user.role_id != 1:
        return False
    return True
