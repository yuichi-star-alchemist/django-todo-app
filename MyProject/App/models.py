from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
# gettext_lazy as _ により_()の中の英文は翻訳される機能がある

class AdminSiteUsers(AbstractUser):
    class Meta:
        verbose_name = "管理者ユーザー"
        verbose_name_plural = "管理者ユーザーテーブル"


class AppUsers(AbstractUser):
    class Meta:
        verbose_name = "アプリユーザー"
        verbose_name_plural = "アプリユーザーテーブル"
        
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ユーザーID'
    )
    email = models.EmailField(
        max_length=64,
        unique=True,
        error_messages={
            'unique': '既に登録されているメールアドレスです',
        },
        verbose_name='メールアドレス'
    )
    username = models.CharField(
        max_length=64,
        verbose_name='ユーザー名'
    )
    password = models.CharField(
        max_length=128,
        verbose_name='パスワード'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        # related_nameがかぶるエラーのために追加 あまりよくわかっていない
        related_name="app_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="app_user_set",
        related_query_name="user",
    )
    
    USERNAME_FIELD = 'email'# 主にこの変数の値が認証の主軸になる
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return str(self.pk)


class Tasks(models.Model):
    class Meta:
        verbose_name_plural = "Taskテーブル"
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='タスクID'
    )
    title = models.CharField(
        max_length=16,
        verbose_name='タイトル'
    )
    detail = models.CharField(
        max_length=128,
        verbose_name='タスク詳細'
    )
    end_time = models.DateField(
        verbose_name='タスクの期限'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時'
    )
    user_id = models.ForeignKey(
        AppUsers,
        on_delete=models.CASCADE,
        verbose_name='ユーザーID'
    )