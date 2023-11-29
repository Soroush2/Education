from django.contrib.auth.models import User


# custom authentication
class EmailBackend:
    # check if user exists
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None

        except User.DoesNotExist:
            return None

    # check user by id
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
