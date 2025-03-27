from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model with a user_type field
    """
    class UserTypes(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        STUDENT = 'STUDENT', _('Student')
        SUPERVISOR = 'SUPERVISOR', _('Supervisor')
        CLIENT = 'CLIENT', _('Client')
    
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserTypes.choices,
        default=UserTypes.STUDENT,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
