from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse, JsonResponse  # noqa
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
import json
from django.db import transaction

from Challenge.forms import ChallengeForm
from Challenge.models import Challenge, Committee, Portfolio
from Core.logger_util import MUNLogger
from Student.models import Students
from django.views.decorators.csrf import csrf_exempt

from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable

logger = MUNLogger(__name__)

# Create your views here.


@method_decorator(login_required, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class Home(View):
    def get(self, request):
        form = ChallengeForm()
        challenges_set = Challenge.objects.all()
        return render(
            request, "chall_desc/index.html",
            {"form": form, "chls": challenges_set}
        )

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


@method_decorator(csrf_exempt, name="dispatch")
class Login_View(View):
    def check_team_and_return_response(self, request, user, username):
        print(username)
        q_filter = Q()
        q_filter &= Q(Q(email=username) | Q(name=username))
        # q_filter &= ~Q(name="naman")
        current_student = Students.objects.filter(q_filter)
        print("current_student-----------", current_student)
        if len(current_student) == 1 and current_student[0].team:
            student_name = current_student[0]
            team_id = current_student[0].team
            print("working fine", student_name, team_id)
            return self.create_response_for_team(
                request, student_name, team_id
            )

        else:
            print("comming inside else")
            login(request, user)
            return redirect("home")

    def create_response_for_team(self, request, student_name, team_id):
        challenge_name, members, status = None, None, None

        challenge = AllTracker.objects.filter(team=team_id)
        print("challenge--------", challenge)
        if challenge:
            challenge_name = challenge[0].challenge
            if (
                challenge.count() > 1
                and challenge[0].student != challenge[1].student
            ):
                members = [c.student for c in challenge]
                return render(
                    request,
                    "success_mates/index.html",
                    {
                        "user": student_name.name,
                        "cname": challenge_name,
                        "members": members,
                        "status": status,
                    },
                )

            else:
                # student_name = challenge[0].student
                return self.get_challenge_status(request, student_name)

    def get_challenge_status(
            self, request, student) -> HttpResponseRedirect | HttpResponse:
        """
            returns the status of already filled MUN Committee
            args:
                student_name | Students.models.Student()

            return:
                dict => Alloted
                None => Not Alloted
        """

        def get_allotment_data(challenge_table) -> dict | None:
            status = challenge_table.values(
                "committee", "portfolio", "status").first()
            if status and status.get("status") == "AL":
                committee_id, portfolio_id = status["committee"], status["portfolio"]  # noqa
                committee = Committee.objects.get(pk=committee_id)
                portfolio = Portfolio.objects.get(pk=portfolio_id)
                return {"committee": committee, "portfolio": portfolio}
            return None

        mun_data = get_allotment_data(
            MUNChallengeTable.objects.filter(student=student),
        )

        if mun_data:
            print("Alloted")
            return render(request, 'mun_alloted/index.html', mun_data)

        ic_data = get_allotment_data(
            ImpactChallengeTable.objects.filter(student=student)
        )

        if ic_data:
            print("Alloted")
            return render(request, 'chall_alloted/index.html', ic_data)

        print("Not Alloted")
        return redirect("sit-back-relax")

    def login_failed_response(self, request):
        error_message = "Incorrect username or password. Please try again."
        return render(
            request,
            "login_signup/index.html",
            {"error_message": error_message}
        )

    def get(self, request):
        print("Inside Login View")
        return render(request, "login_signup/index.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("&*" * 15)
        print(username, password)

        # Check whether this User has teams as None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return self.check_team_and_return_response(request, user, username)
        else:
            return self.login_failed_response(request)


@login_required
@csrf_exempt
def success(request):
    logout(request)
    return render(request, "success_congrats/index.html")

@csrf_exempt
def sit_back_relax(request):
    return render(request, "success_congrats/index.html")


@login_required
@csrf_exempt
def logout_user(request):
    logout(request)
    return redirect("login")


def test(request):
    return HttpResponse("Site is working fine")


def random_teamID_generator() -> str:
    import random
    import string

    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(5))

@csrf_exempt
def load_portfolios(request):
    committee_id = request.GET.get('committee_id')
    committee = Committee.objects.get(pk=int(committee_id))
    portfolios = Portfolio.objects.filter(committee=committee).order_by('name')
    if not portfolios:
        portfolios = Portfolio.objects.filter(committee=None).order_by('name')

    portfolio_list = [{'id': portfolio.id, 'name': portfolio.name}
                      for portfolio in portfolios]

    return JsonResponse({'portfolios': portfolio_list})


@csrf_exempt
@login_required
def submit_preference(request):
    if request.method == 'POST':

        # get student and its school

        ajax_response_string = request.POST.get('all_list')

        if ajax_response_string:
            current_student = Students.objects.get(Q(email=request.user.email) | Q(email=request.user.username))
            current_school = current_student.school

            challenge_name = request.session.get("first_page_data", {}).get('challenge', {}).get('name')
            MODEL = (
                ImpactChallengeTable
                if "impact" in challenge_name.lower()
                else MUNChallengeTable
            )
            ajax_dict = json.loads(ajax_response_string)

            personal_info = ajax_dict[-1].get("personal_info")

            with transaction.atomic():
                team_id = random_teamID_generator()
                current_student.team = team_id
                current_student.save()
                for p in ajax_dict:
                    if "preference" in p:
                        pref = p.get("preference")
                        com = Committee.objects.get(pk=int(p.get("committee")))
                        prt = Portfolio.objects.get(pk=int(p.get("portfolio")))

                        a = AllTracker.objects.create(
                            student=str(current_student),
                            school=str(current_school),
                            challenge=str(challenge_name),
                            committee=str(com.name),
                            portfolio=str(prt.name),
                            preference=int(int(pref)),
                            team=team_id,
                        )
                        a.save()
                    else:
                        break

                t = MODEL.objects.create(
                    student=current_student,
                    school=current_school,
                    all_tracker=a,
                )

                if personal_info:
                    t.remarks = (
                        f"Personal achivements and accolades {personal_info}"
                    )
                t.save()

        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})

@csrf_exempt
def custom_500_error(request, *args, **kwargs):
    return render(request, '500.html', status=500)
