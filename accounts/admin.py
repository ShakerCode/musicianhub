from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from musicianhub.forms import BandCreationForm, BandChangeForm


from .models import MusicUser, Band
from .forms import MusicUserCreationForm, MusicUserChangeForm


class MusicUserAdmin(OSMGeoAdmin):
    add_form = MusicUserCreationForm
    form = MusicUserChangeForm
    model = MusicUser


    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'instrument', 'email', 'age', 'band', 'location')}),
    )

    list_display = ['username', 'first_name', 'last_name', 'instrument', 'email', 'age', 'band', 'location']

class MusicUserInline(admin.TabularInline):
    model = MusicUser
    extra = 3

class BandAdmin(OSMGeoAdmin):
    add_form = BandCreationForm
    form = BandChangeForm
    model = Band

    fieldsets = (
        (None, {'fields': ('bandname', 'location', 'city', 'genre', 'description', 'total_members', 'leader')}),
    )

    inlines = [MusicUserInline]
    list_display = ['bandname', 'total_members', 'leader']


admin.site.register(MusicUser, MusicUserAdmin)
admin.site.register(Band, BandAdmin)
