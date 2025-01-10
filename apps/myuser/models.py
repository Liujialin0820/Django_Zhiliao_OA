from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.hashers import (
    make_password,
)
from shortuuidfield import ShortUUIDField


# Create your models here.
# 重写user模型
class UserStatusChoice(models.IntegerChoices):
    ACTIVED = 1
    UNACTIVE = 2
    LOCKED = 3


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserStatusChoice.ACTIVED)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField(
        ("username"),
        max_length=150,
        unique=False,
    )
    first_name = models.CharField(("first name"), max_length=150, blank=False)
    last_name = models.CharField(("last name"), max_length=150, blank=True)
    email = models.EmailField(("email address"), unique=True, blank=False)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    status = models.IntegerField(
        choices=UserStatusChoice, default=UserStatusChoice.UNACTIVE
    )
    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    department = models.ForeignKey("MyDepartment", on_delete=models.SET_NULL, null=True)

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    # 用来鉴权的
    USERNAME_FIELD = "email"
    # 指定那些字段是必须传的, 但是不能重复包含
    REQUIRED_FIELDS = ["username", "password"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name


class MyDepartment(models.Model):
    name = models.CharField(max_length=100)
    intro = models.CharField(max_length=300)
    leader = models.OneToOneField(
        MyUser,
        null=True,
        on_delete=models.SET_NULL,
        related_name="department_leader",  # 自定义反向名称
    )
    manager = models.ForeignKey(
        MyUser,
        null=True,
        on_delete=models.SET_NULL,
        related_name="department_manager",  # 自定义反向名称
    )
