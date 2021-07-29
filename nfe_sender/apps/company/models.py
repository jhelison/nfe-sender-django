from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import re


def CNPJ_validator(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.
    """
    cnpj = "".join(re.findall("\d", str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = map(int, cnpj)
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cnpj
    return False


class UserManager(BaseUserManager):
    def _create_user(
        self, username, email, password, is_staff, is_superuser, **extra_fields
    ):
        now = timezone.now()
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(
            username, email, password, False, False, **extra_fields
        )

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # cnpj = models.CharField(max_length=14, validators=[CNPJ_validator], unique=True)
    #Base django user filds
    username = models.CharField(
        "username",
        max_length=15,
        unique=True,
        help_text="Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters",
    )
    first_name = models.CharField("first name", max_length=30)
    last_name = models.CharField("last name", max_length=30)
    email = models.EmailField("email address", max_length=255, unique=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    #Custom user filds
    is_trusty = models.BooleanField(
        "trusty",
        default=False,
        help_text="Designates whether this user has confirmed his account.",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    # def get_full_name(self):
    #     full_name = "%s %s" % (self.first_name, self.last_name)
    #     return full_name.strip()

    # def get_short_name(self):
    #     return self.first_name
