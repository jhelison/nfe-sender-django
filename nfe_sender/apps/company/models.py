from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager
from .choices import BrazilianStates

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("cnpj", unique=True, max_length=14)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    #custom fields
    is_company = models.BooleanField(default=True)
    company_name = models.CharField(blank=True, max_length=80)
    uf = models.IntegerField(choices=BrazilianStates.choices, default=21)
    is_hom = models.BooleanField(default=True)
    base64_certificate = models.TextField(blank=True)
    certificate_password = models.CharField(blank=True, max_length=80)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
        
    def __str__(self):
        return self.username