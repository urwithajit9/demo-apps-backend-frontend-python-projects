from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

# AbstractUser is a full User model, complete with fields,
# like an abstract class so that you can inherit from it
#  and add your own profile fields and methods.


from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.email


