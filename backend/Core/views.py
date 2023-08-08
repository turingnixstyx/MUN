from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from Challenge.forms import ChallengeForm
from Student.models import Students
from Challenge.models import Challenge
# Create your views here.


@method_decorator(login_required, name="dispatch")
class Home(View):
    def get(self, request):
        form = ChallengeForm()
        challenges_set = Challenge.objects.all()
        return render(request, "home.html", {"form": form, 'chls' : challenges_set})

    def post(self, request):
        challenge = request.POST.get("challenge")
        # get challenge name
        challenge_object= Challenge.objects.get(pk=int(challenge))
        print("Got challenge", challenge_object.name, challenge_object.id)
        self.request.session["first_page_data"] = {
            "challenge": {"name": challenge_object.name}
        }
        print('self.request.session["first_page_data"] --------', self.request.session["first_page_data"])
        if challenge_object.id in [1, 4]:
            return redirect("committee")
        else:
            return redirect("teams")

        # Add challenge name to session
        # MUN = 4
        # IC = 1

        # redirect on basis of challenge

        return render(request, "home.html")


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

@login_required
def success(request):
    return render(request, "success.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


def test_view(request):
    return render(request, 'preferences.html')
