from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from Challenge.forms import ChallengeForm
from Challenge.models import Challenge, Committee, Portfolio
from Core.logger_util import MUNLogger
from Student.models import Students

from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable

logger = MUNLogger(__name__)

# Create your views here.


@method_decorator(login_required, name="dispatch")
@logger.handle_exceptions_class
class Home(View):
    def get(self, request):
        form = ChallengeForm()
        challenges_set = Challenge.objects.all()
        return render(request, "home.html", {"form": form, "chls": challenges_set})

    def post(self, request):
        challenge = request.POST.get("challenge")
        # get challenge name
        challenge_object = Challenge.objects.get(pk=int(challenge))
        print("Got challenge", challenge_object.name, challenge_object.id)
        self.request.session["first_page_data"] = {
            "challenge": {"name": challenge_object.name}
        }
        print(
            'self.request.session["first_page_data"] --------',
            self.request.session["first_page_data"],
        )
        if (
            "united" in challenge_object.name.lower()
            or "impact" in challenge_object.name.lower()
            or "model" in challenge_object.name.lower()
        ):
            return redirect("committee")
        else:
            return redirect("teams")


class Login_View(View):
    def check_team_and_return_response(self, request, user, username):
        q_filter = Q()
        q_filter &= Q(Q(email=username) | Q(name=username))
        q_filter &= ~Q(name="naman")
        current_student = Students.objects.filter(q_filter).values("name", "team")

        if len(current_student) == 1 and current_student[0].get("team"):
            student_name = current_student[0].get("name")
            team_id = current_student[0].get("team")
            return self.create_response_for_team(request, student_name, team_id)

        else:
            login(request, user)
            return redirect("home")

    def create_response_for_team(self, request, student_name, team_id):
        challenge_name, members, status = None, None, None

        challenge = AllTracker.objects.filter(team=team_id)
        print(challenge)
        if challenge:
            challenge_name = challenge[0].challenge
            if challenge.count() > 1 and challenge[0].student != challenge[1].student:
                members = [c.student for c in challenge]
            else:
                student_name = challenge[0].student
                status = self.get_challenge_status(student_name)

        return render(
            request,
            "returning_user.html",
            {
                "user": student_name,
                "cname": challenge_name,
                "members": members,
                "status": status,
            },
        )

    def get_challenge_status(self, student_name):
        mun_status = MUNChallengeTable.objects.filter(student=student_name).values(
            "committee", "portfolio", "status"
        )
        if len(mun_status) > 0:
            if mun_status[0].get("status") == "AL":
                cid = mun_status[0].get("committee")
                pid = mun_status[0].get("portfolio")

                committee = Committee.objects.get(pk=cid)
                portfolio = Portfolio.objects.get(pk=pid)

                return {"committee": committee, "portfolio": portfolio}
            else:
                return None
        ic_status = ImpactChallengeTable.objects.filter(student=student_name).values(
            "committee", "portfolio", "status"
        )

        if len(ic_status) > 0:
            if ic_status[0].get("status") == "AL":
                cid = ic_status[0].get("committee")
                pid = ic_status[0].get("portfolio")

                committee = Committee.objects.get(pk=cid)
                portfolio = Portfolio.objects.get(pk=pid)

                return {"committee": committee, "portfolio": portfolio}
            else:
                return None

    def login_failed_response(self, request):
        print("login_failed_response")
        error_message = "Incorrect username or password. Please try again."
        return render(request, "login.html", {"error_message": error_message})

    def get(self, request):
        print("Inside Login View")
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check whether this User has teams as None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return self.check_team_and_return_response(request, user, username)
        else:
            return self.login_failed_response(request)


@login_required
@logger.handle_exceptions_class
def success(request):
    # logout(request)
    return render(request, "success.html")


@login_required
@logger.handle_exceptions_class
def logout_user(request):
    logout(request)
    return redirect("login")


def test(request):
    return HttpResponse("Site is working fine")
