from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


# Create your models here.
class UserManager(BaseUserManager):
    # カスタムユーザーマネージャー
    use_in_migrations = True  # このクラスもマイグレーションで管理できるようになる

    def _create_user(self, email, password, **extra_fields):
        # emailを必須にする
        if not email:
            raise ValueError(_('メールアドレスは必須です'))
        # emailでUserモデルを作成
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
    created_at = models.DateTimeField("作成日", auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    # カスタムユーザーモデル
    email = models.EmailField("email", unique=True)
    name = models.CharField("ユーザー名", max_length=20, default=_("ユーザー"))
    house = models.ForeignKey(House, on_delete=PROTECT, blank=True, null=True)
    housechore_title = models.CharField(
        "家事", max_length=100, default=_("割り当てられていません"))
    housechore_desc = models.CharField("詳細", max_length=100, default=_("詳細なし"))
    done_weekly = models.BooleanField("毎週の家事完了", default=False)
    done_monthly = models.BooleanField("公益費の支払い完了", default=False)
    # ハウス管理者権限を付与する場合、Trueにする。
    is_staff = models.BooleanField("ハウス管理者権限", default=False)
    # 仮登録状態→本登録でTrueにする。
    is_active = models.BooleanField("本登録完了", default=True)
    date_joined = models.DateTimeField("仮登録日", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
