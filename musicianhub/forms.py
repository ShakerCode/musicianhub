from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.gis import forms as gis_forms
from django.forms import ModelForm
from accounts.models import MusicUser, Band
import re

class BandCreationForm(ModelForm):

    def is_valid(self, bandname, city, genre):
        print("HERE")
        taken = Band.objects.filter(bandname__iexact=bandname).exists()
        print(taken)
        validfields = not (bandname.isspace() or city.isspace() or genre.isspace()) and re.match(r'^[a-zA-Z-_ ]+$', city) and re.match(r'^[a-zA-Z-_ ]+$', genre)
        return not taken and validfields # if band name has not been taken and it's not completely whitespace

    class Meta:
        model = Band
        # point = gis_forms.PointField(widget=gis_forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))
        fields = ['bandname', 'location', 'genre', 'description', 'city', 'leader']

class BandChangeForm(ModelForm):

    class Meta:
        model = Band
        fields = ['bandname', 'location', 'genre', 'description', 'city', 'leader']
