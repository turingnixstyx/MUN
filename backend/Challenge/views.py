from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from Core.models import AllTracker, ImpactChallengeTable, MUNChallengeTable
from Student.models import Students

from .forms import (
    AddonForms,
    ExtendedTeamForm,
    PreferenceForm,
    TeamForm,
    PersonalInfoForm,
)
from .models import Committee, Portfolio

# Create your views here.


@method_decorator(login_required, name="dispatch")
class CommitteeView(FormView):
    template_name = "preferences.html"
    form_class = PreferenceForm
    success_url = reverse_lazy("success")

    def get_student_and_school(self):
        current_user = self.request.user
        print(current_user)
        self.current_student = Students.objects.get(email=current_user.username)
        self.current_school = self.current_student.school
        self.challenge_name = (
            self.request.session["first_page_data"].get("challenge", {}).get("name")
        )

    def form_valid(self, form):
        # Process the form data here (save to database, send an email, etc.)
        committee_list = self.request.POST.getlist("committee")
        portfolio_list = self.request.POST.getlist("portfolio")
        personal_info = self.request.POST.get("text")

        self.query_runner(committee_list, portfolio_list, personal_info)
        # Add your processing logic here
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cname = self.request.session["first_page_data"].get("challenge", {}).get("name")
        if "model" in cname.lower() or "united" in cname.lower():
            info = PersonalInfoForm()
            context["info"] = info

        return context

    def random_teamID_generator(self):
        import random
        import string

        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(5))

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        cname = self.request.session["first_page_data"].get("challenge", {}).get("name")
        MODEL = (
            MUNChallengeTable
            if "united" in cname or "model" in cname
            else ImpactChallengeTable
        )

        committee_queryset = Committee.objects.exclude(
            id__in=MODEL.objects.values("id")
        )
        portfolio_querset = Portfolio.objects.exclude(id__in=MODEL.objects.values("id"))

        kwargs["com_queryset"] = committee_queryset
        kwargs["por_queryset"] = portfolio_querset

        return kwargs

    def query_runner(self, committee_list, portfolio_list, *args, **kwargs):
        team_id = self.random_teamID_generator()
        self.get_student_and_school()
        personal_info = ""
        with transaction.atomic():
            if args:
                personal_info = args[0]
                cs = self.current_student
                cs.personal_info = personal_info
                cs.save()

            preference = 1
            MODEL = ImpactChallengeTable if "impact" in self.challenge_name.lower() else MUNChallengeTable
            print(MODEL)
            for committees, portfolios in zip(committee_list, portfolio_list):
                com = Committee.objects.get(pk=int(committees))
                prt = Portfolio.objects.get(pk=int(portfolios))

                # add to Total Global tracker
                a = AllTracker.objects.create(
                    student=str(self.current_student),
                    school=str(self.current_school),
                    challenge=str(self.challenge_name),
                    committee=str(com.name),
                    portfolio=str(prt.name),
                    preference=preference,
                    team=team_id,
                )
                
                if personal_info:
                    a.remarks = f"Personal achivements and accolades {personal_info}"
                a.save()

                preference += 1

            t = MODEL.objects.create(
                    student=str(self.current_student),
                    school=str(self.current_school),
                )
            
            if personal_info:
                t.remarks = f"Personal achivements and accolades {personal_info}"

            t.save()

    def check_validity(self, committee, portfolio, challenge):
        c = None

        if "impact" in challenge.lower():
            c = ImpactChallengeTable.objects.filter(
                committee=committee, portfolio=portfolio
            )

        elif "mun" in challenge.lower() or "united" in challenge.lower():
            c = MUNChallengeTable.objects.filter(
                committee=committee, portfolio=portfolio
            )

        return False if c else True


@method_decorator(login_required, name="dispatch")
class TeamView(FormView):
    template_name = "teams.html"
    success_url = reverse_lazy("success")

    def get_form_class(self):
        cname = self.request.session["first_page_data"].get("challenge", {}).get("name")
        if "theatrics" in cname.lower():
            print("getting here")
            return ExtendedTeamForm
        else:
            return TeamForm

    def get_student_and_school(self):
        current_user = self.request.user
        print(current_user)
        self.current_student = Students.objects.get(email=current_user.email)
        self.current_school = self.current_student.school
        self.challenge_name = (
            self.request.session["first_page_data"].get("challenge", {}).get("name")
        )

    def random_teamID_generator(self):
        import random
        import string

        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(5))

    def form_valid(self, form):
        # Process the form data here (save to database, send an email, etc.)
        members = []
        for idx in range(5):
            key = "student" + str(idx + 1)
            if self.request.POST.get(key):
                members.append(self.request.POST.get(key))

        print(members)
        self.query_runner(members)
        # Add your processing logic here
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        q_filter = Q()
        self.get_student_and_school()
        q_filter &= Q(school=self.current_school)
        q_filter &= ~Q(email=self.current_student.email)
        q_filter &= Q(team=None)

        custom_queryset = Students.objects.filter(q_filter)
        kwargs["queryset"] = custom_queryset
        return kwargs

    def query_runner(self, team_members, *args, **kwargs):
        with transaction.atomic():
            self.get_student_and_school()
            team_id = self.current_student.name

            self.current_student.team=team_id
            self.current_student.save()

            print("outside for loop")
            for member in team_members:
                # get team leader from user
                print("inside for loop")

                member_name = Students.objects.get(pk=member)
                member_name.team = team_id

                # add all team members to
                a = AllTracker.objects.create(
                    student=member_name.name,
                    school=member_name.school.name,
                    challenge=self.challenge_name,
                    team=team_id,
                )
                a.save()
                member_name.save()


@method_decorator(login_required, name="dispatch")
class AddOnView(FormView):
    template_name = "add_ons.html"
    form_class = AddonForms
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        return super().form_valid(form)
