from importlib.resources import _

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractUser, Permission, Group, PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not kwargs.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **kwargs)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class Create(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True, unique=True)
    phone_number = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=128, null=True)
    photo = models.ImageField(upload_to='profile/', blank=True, null=True,
                              default='assets/img/default.jpg')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Add this field

    USERNAME_FIELD = 'email'  # specify the username field
    REQUIRED_FIELDS = ['first_name', ]
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='users_groups'  # add this line
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='users_permissions'  # add this line
    )

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True if self.pk else False

    @property
    def is_anonymous(self):
        return False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.name


class Projects(models.Model):
    name = models.CharField(max_length=255)


class Add_Lists(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='add_list', default=True ,
                                blank=True, null=True )

    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.ForeignKey(Add_Lists, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(Create, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('edited', 'Edited '),
        ('in_progress', 'In_progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)
    PRIORITY_CHOICES = [
        ('none', 'None'),
        ('low', 'Low'),
        ('medium', 'Medium '),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES)
    attachment = models.FileField(upload_to='profile', null=True)

    def __str__(self):
        return self.title
