from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def get_or_none(self, arg=None, **kwargs):
        try:
            if arg:
                return self.get(arg) # NOTE: adds Q object support
            if kwargs:
                return self.get(kwargs)
        except Exception as e:
            return None
