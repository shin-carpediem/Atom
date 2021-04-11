from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('メールアドレスは必須です'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class House(models.Model):
    name = models.CharField("ハウス名", max_length=20, default="House")
    common_fee = models.PositiveIntegerField(default=500)
    common_fee_date = models.PositiveIntegerField(default=25)
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return self.name + str(self.common_fee) + str(self.common_fee_date)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email", unique=True)
    name = models.CharField("ユーザー名", max_length=20, default=_("ユーザー"))
    house = models.ForeignKey(House, on_delete=PROTECT, blank=True, null=True)
    house_common_fee = models.PositiveIntegerField(default=500, blank=True, null=True)
    house_common_fee_date = models.PositiveIntegerField(default=25, blank=True, null=True)
    housechore_title = models.CharField(
        "家事", max_length=100, default=_("割り当てられていません"))
    housechore_desc = models.CharField("詳細", max_length=100, default=_("詳細なし"))
    done_weekly = models.BooleanField(
        "毎週の家事完了", default=False, blank=True, null=True)
    done_monthly = models.BooleanField(
        "公益費の支払い完了", default=False, blank=True, null=True)
    is_staff = models.BooleanField("ハウス管理者権限", default=False)
    is_active = models.BooleanField("本登録完了", default=True)
    date_joined = models.DateTimeField("仮登録日", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
