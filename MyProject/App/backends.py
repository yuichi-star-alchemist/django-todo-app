from django.contrib.auth.backends import ModelBackend

from .models import AppUsers

UserModel = AppUsers

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def with_perm(self, perm, is_active=True, include_superusers=True, obj=None):
        if isinstance(perm, str):
            try:
                app_label, codename = perm.split(".")
            except ValueError:
                raise ValueError(
                    "Permission name should be in the form "
                    "app_label.permission_codename."
                )
        elif not isinstance(perm, Permission):
            raise TypeError(
                "The `perm` argument must be a string or a permission instance."
            )

        if obj is not None:
            return UserModel._default_manager.none()

        permission_q = Q(group__user=OuterRef("pk")) | Q(user=OuterRef("pk"))
        if isinstance(perm, Permission):
            permission_q &= Q(pk=perm.pk)
        else:
            permission_q &= Q(codename=codename, content_type__app_label=app_label)

        user_q = Exists(Permission.objects.filter(permission_q))
        if include_superusers:
            user_q |= Q(is_superuser=True)
        if is_active is not None:
            user_q &= Q(is_active=is_active)

        return UserModel._default_manager.filter(user_q)

    def get_user(self, user_id):
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None