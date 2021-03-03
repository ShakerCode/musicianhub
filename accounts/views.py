from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MusicUserCreationForm

class RegisterView(CreateView):
    form_class = MusicUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        if new_user is not None:
            login(self.request, new_user)
        return valid


# def register(request):
#     if request.method == "POST":
#         form = MusicUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect("/")
#     else:
#         form = MusicUserCreationForm()
#     return render(request, "registration/register.html", {"form":form})


# def search(request):
#     return render(request, "search.html", {})

# def index(request):
#     return render(request, "index.html", {}) 