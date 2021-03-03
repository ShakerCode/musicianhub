from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from accounts.models import MusicUser, Band
from django.db.models import Q, F
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .forms import BandCreationForm
from django.views.decorators.csrf import csrf_exempt
import json


def about(request):
    return render(request, 'about.html')

def search(request):
    return render(request, 'search.html', {'all_objects': {}})

def search_user(request):
    if request.method == 'GET':
        if 'reset' in request.GET:
            return redirect('search')
        all_objects = None
        instrument, age, proximity, in_band = request.GET.get('instrument'), request.GET.get('age'), request.GET.get('proximity'), request.GET.get('in_a_band')
        user_pk = request.GET.get('userpk')
        print(instrument, age, proximity, in_band)
        all_objects = filter_user_list(instrument, age, proximity, in_band, user_pk)
    return render(request, 'search.html', {'all_objects': all_objects})


def bands(request):
    return render(request, 'bands.html', {'all_objects': {}})

def search_band(request):
    if request.method == 'GET':
        if 'reset' in request.GET:
            return redirect('bands')
        all_objects = None
        bandname, genre, proximity, total_members = request.GET.get('bandname'), request.GET.get('genre'), request.GET.get('proximity').strip(), request.GET.get('total_members')
        if bandname != '':
            sortType, user_pk = request.GET.get('sortType'), request.GET.get('userpk')
            # user_pk = request.GET.get('userpk')
            print(bandname, genre, proximity, total_members)
            all_objects = filter_band_list(bandname, genre, proximity, total_members, user_pk)
            all_objects = sort_band_list(all_objects, sortType, user_pk)
    return render(request, 'bands.html', {'all_objects': all_objects})


def join_band(request):
    print("IM HERE")
    print(request.method)
    if request.method == 'POST':
        band_pk, user_pk = request.POST.get(
            'band_pk'), request.POST.get('user_pk')
        print(band_pk)
        print(user_pk)

        user, new_band = MusicUser.objects.get(
            pk=user_pk), Band.objects.get(pk=band_pk)

        join_band_helper(user, new_band)

    returnInfo = {  # change to return ALL bands
        'bandname': new_band.bandname,
        'total_members': new_band.total_members,
        'pk': new_band.pk
    }

    # return render(request, 'bands.html', {'total_members': []})
    return JsonResponse(returnInfo)

def leave_band(request):
    if request.method == 'POST':
        user = MusicUser.objects.get(pk=request.POST.get('user_pk'))
        old_band = Band.objects.get(pk=user.band.pk)

        leave_band_helper(user, old_band)

    return HttpResponse("Successfully left band")

def filter_user_list(instrument, age, proximity, in_band, user_pk):
    returnList = None
    user = MusicUser.objects.get(pk=user_pk)
    not_in_band = (in_band == 'no') # true if user is NOT in band. isnull will be TRUE
    if age != '60+':
        ar = age.split(",")
        returnList = MusicUser.objects.all().filter(instrument__icontains=instrument, age__range=(int(ar[0]), int(ar[1])), location__distance_lte=(user.location, D(mi=int(proximity))), band__isnull=not_in_band)
    if age == '60+':
        returnList = MusicUser.objects.all().filter(instrument__icontains=instrument, age__gte=60, location__distance_lte=(user.location, D(mi=int(proximity))), band__isnull=not_in_band)
    return returnList

def sort_band_list(all_objects, sortType, user_pk):
    returnList = None
    user = MusicUser.objects.get(pk=user_pk)
    if sortType == 'location':
        returnList = all_objects.annotate(distance=Distance('location', user.location)).order_by('distance')
    elif sortType == 'genre':
        returnList = all_objects.order_by('genre')
    elif sortType == 'total_members':
        returnList = all_objects.order_by('-total_members')
    else: # default case is to sort by band name. Will cover 'bandname' option as well
        returnList = all_objects.order_by('bandname')
    return returnList

def filter_band_list(bandname, genre, proximity, total_members, user_pk):
    returnList = None
    user = MusicUser.objects.get(pk=user_pk)
    if bandname != '':
        returnList = Band.objects.filter(bandname__icontains=bandname, genre__icontains=genre, total_members__lte=total_members, location__distance_lte=(user.location, D(mi=int(proximity))))
    if bandname == '':
        returnList = Band.objects.filter(genre__icontains=genre, total_members__lte=total_members, location__distance_lte=(user.location, D(mi=int(proximity))))
    return returnList

# def filter_user_list(instrument, age, proximity, in_band):


class CreateBandView(CreateView):
    form_class = BandCreationForm
    template_name = 'create_band.html'
    # success_url = reverse_lazy('/')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        bandname1, city1, genre1, description1, lng, lat, user_pk = request.POST.get('bandname'), request.POST.get(
            'city'), request.POST.get('genre'), request.POST.get('description'), request.POST.get('lng'), request.POST.get('lat'), request.POST.get('user_pk')
        user = MusicUser.objects.get(pk=user_pk)
        location1 = None
        if lng != '' and lat != '':
            # longitude is x and latitude is y
            location1 = Point(float(lng), float(lat), srid=4326)
        print(lng, lat)
        if form.is_valid(bandname1, city1, genre1): # custom is_valid() in forms.py
            new_band = Band(bandname=bandname1.strip(), description=description1.strip(), location=location1, city=city1, genre=genre1, total_members=0, leader=user.email)
            new_band.save()
            join_band_helper(user, new_band)

            return HttpResponse('Band created successfully!')
        else:
            return HttpResponse('Band name either taken or field(s) is invalid.')

    # should be the same as a returning an object with render()
    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(
            serialize("geojson", Band.objects.all()))
        return context


def join_band_helper(user, new_band): # helper method for whenever a user joins/creates a new band
    old_band = user.band
    user.band = new_band  # user joins new band
    user.save()

    if old_band is not None:
        old_band.total_members -= 1  # decrease old band's total members
        if old_band.total_members == 0:
            old_band.leader = None
        # if old_band.total_members == 1:
        #     # give leadership to remaining member
        #     old_band.leader = Band.objects.get(pk=old_band.pk).musicuser_set.first().email
        else:
            old_band.leader = Band.objects.get(pk=old_band.pk).musicuser_set.first().email
        old_band.save()

    print("TOTAL BAND MEMBERS:" + str(new_band.total_members))
    new_band.total_members += 1
    if new_band.total_members == 1:  # user is first person to join
        new_band.leader = user.email

    new_band.save()

def leave_band_helper(user, old_band):
    user.band = None
    old_band.total_members -= 1
    if old_band.total_members == 0:
        old_band.leader = None
    else:
        old_band.leader = Band.objects.get(pk=old_band.pk).musicuser_set.first().email
    user.save()
    old_band.save()


def band_profile(request, pk):
    band = Band.objects.get(pk=pk)
    member_list = band.musicuser_set.all()
    return render(request, 'band_profile.html', {'band': band, 'member_list': member_list})

def user_profile(request, pk):
    user = MusicUser.objects.get(pk=pk)
    return render(request, 'user_profile.html', {'searched_user': user})

def my_profile(request):
    return render(request, 'profile.html')

def autocomplete(request):
    if 'term' in request.GET:
        q = request.GET.get('term')
        st = request.GET.get('searchType')
        print(q)
        print(request.GET.get('searchType'))
        results = []
        if st == 'userSearch':
            for r in MusicUser.objects.filter(Q(instrument__istartswith=q)).order_by('instrument'):
                if r.instrument not in results:
                    results.append(r.instrument)
        if st == 'bandsSearch':
            for r in Band.objects.filter(Q(bandname__istartswith=q)).order_by('bandname'):
                if r.bandname not in results:
                    results.append(r.bandname)
        # needed since JsonResponse expects dictionary
        return JsonResponse(results, safe=False)
    return render(request, 'index.html')

# def instrument_search(request):
#     return render(request, 'search.html')


# def index(request):
#     return render(request, "index.html", {})


# class SearchView(ListView):
#     model = MusicUser
#     template_name = 'search.html'
#     print("lmao")

    # def get_context_data(self):
    #     context = super().get_context_data()
    #     context.update({
    #         'search': self.request.GET.get('search', '')
    #     })
    #     return context

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         all_objects = MusicUser.objects.filter(instrument__icontains=query)
    #         print(all_objects)
    #     else:
    #         all_objects = None
    #     return all_objects

# def create_band(request):
#     # form = BandCreationForm()
#     if request.method == 'POST':
#         print(request.POST)
#         bandname1, city1, genre1 = request.POST.get('bandname'), request.POST.get('city'), request.POST.get('genre')
#         print(bandname1, city1, genre1)

#         if not Band.objects.filter(bandname__iexact=bandname1).exists():
        # newband = Band(bandname=bandname1, city=city1, genre=genre1, total_members=0)
        # newband.save()
#             return HttpResponse('Band created successfully!')
#         else:
#             print('here')
#             return HttpResponse('Band name taken')

    # return render(request, 'create_band.html')