from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from Challenge.forms import ChallengeForm

# Create your views here.


@method_decorator(login_required, name="dispatch")
class Home(View):
    def get(self, request):
        form = ChallengeForm()
        return render(request, "home.html", {"form": form})

    def post(self, request):
        form = ChallengeForm(request.POST)
        if form.is_valid():

            challenge = form.cleaned_data["challenge"]
            print("Got challenge", challenge.name)

            if challenge.name == "Challenge 2":  # Impact Challenge
                return redirect("committee")

            else:  # All other else
                return redirect("teams")
        # Add challenge name to session

        # redirect on basis of challenge


class Login_View(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            return HttpResponse("Fuck you Wrong Password")
