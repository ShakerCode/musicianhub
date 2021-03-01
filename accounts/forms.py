from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import forms as gis_forms
from django.forms import ModelForm
from .models import MusicUser, Band

class MusicUserCreationForm(UserCreationForm):

    location = gis_forms.PointField(widget=gis_forms.OSMWidget(attrs={
        'map_width': 1100,
        'map_height': 750,
        'default_lat': 38.9072,
        'default_lon': -77.0369,
        'default_zoom': 6}))
    class Meta:
        model = MusicUser
        fields = ['email', 'username', 'first_name', 'last_name', 'instrument', 'age', 'password1', 'password2', 'location']

class MusicUserChangeForm(UserChangeForm):

    class Meta:
        model = MusicUser
        fields = ['email', 'username', 'first_name', 'last_name', 'instrument', 'age', 'band']