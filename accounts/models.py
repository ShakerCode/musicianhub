from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import AbstractUser, Group, UserManager, BaseUserManager
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator
from django.contrib.gis import forms
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

# class CustomUserManager(BaseUserManager):
#       def create_superuser(self, email, password, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('age', 20)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         super_user = self._create_user(username, email, password, **extra_fields)
#         return super_user

alphanumeric_dash_underscore = RegexValidator(r'^[0-9a-zA-Z-_]+$', "Only alphanumeric characters and '-' and '_' are allowed.")
alphabetical_dash_underscore = RegexValidator(r'^[a-zA-Z-_]+$', "Only alphabetical characters and '-' and '_' are allowed.")

class EmailField(models.EmailField):
    def get_prep_value(self, value):
        value = super(EmailField, self).get_prep_value(value)
        if value is not None:
            value = value.lower()
        return value

class LowerCaseCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerCaseCharField, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        return str(value).lower()

class CapitalizedCityField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(CapitalizedCityField, self).__init__(*args, **kwargs)
    def get_prep_value(self, value):
        print(value)
        temp = ' '.join([x.lower().capitalize() for x in value.split(" ")]).strip()
        return str(temp)

class Band(models.Model):
    bandname = gis_models.CharField(max_length=100, validators=[ASCIIUsernameValidator()])
    description = models.TextField(max_length=1000, blank=True)
    location = gis_models.PointField(default=None)
    genre = CapitalizedCityField(max_length=100, validators=[ASCIIUsernameValidator()])
    city = CapitalizedCityField(max_length=50, validators=[alphabetical_dash_underscore])
    total_members = models.IntegerField(default=0)
    leader = models.EmailField(default=None, null=True, blank=True, max_length=200)

    def __str__(self):
        return str(self.bandname)

class MusicUser(AbstractUser):
    # add additional fields in here
    # username, first_name, and last_name are all built in to AbstractUser


    username = models.CharField(
        ('username'),
        max_length=150,
        unique=True,
        help_text=('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[ASCIIUsernameValidator()],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    first_name = models.CharField(('first name'), max_length=150, blank=True, validators=[alphabetical_dash_underscore])
    last_name = models.CharField(('last name'), max_length=150, blank=True, validators=[alphabetical_dash_underscore])

    instrument = LowerCaseCharField(default=None, null=True, blank=True, max_length=80, validators=[alphabetical_dash_underscore])
    age = models.IntegerField(default=None, null=True, blank=True)
    band = models.ForeignKey(Band, default=None, null=True, blank=True, on_delete=models.CASCADE)
    location = gis_models.PointField(default=None, null=True, blank=True)
    email = EmailField(('Email'), unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return str(self.email)

# class Messages(models.Model):
#     sender = models.ForeignKey(MusicUser, default=None, null=True, blank=True, on_delete=models.CASCADE)
#     receiver = models.ForeignKey(MusicUser, default=None, null=True, blank=True, on_delete=models.CASCADE)
#     message_text = models.TextField(max_length=1000, default=None, null=True, blank=True)
#     timestamp = models.TimeField(auto_now_add=True)