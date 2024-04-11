from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


class EmailAuthBackend(ModelBackend):
    '''
     Custom auth backend for authenticating users based on email rather than username.
     overrides (`modelbackend.authenticate()').
     Authenticates against settings.AUTH_USER_MODEL
    '''
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return UserModel.objects.filter(email=username).order_by('id').first()
        return None