from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False):
                return user
        return None

    def get_user(self, user_id):
        User = get_user_model()    
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
