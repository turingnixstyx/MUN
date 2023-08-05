from typing import Any, Dict

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.db import transaction
from .models import Committee, Portfolio
from Student.models import Students
from Core.models import AllTracker

from .forms import AddonForms, PreferenceForm, TeamForm

# Create your views here.

class CommitteeView(FormView):
    template_name = "preferences.html"
    form_class = PreferenceForm
    success_url = reverse_lazy("success")
    

    def get_student_and_school(self):
        current_user = self.request.user.username
        self.current_student = "Naman" # Students.objects.get(email=current_user)
        self.current_school = "DPS" # self.current_student.school


    def form_valid(self, form):
        # Process the form data here (save to database, send an email, etc.)
        committee_list=self.request.POST.getlist('committee')
        portfolio_list=self.request.POST.getlist('portfolio')

        self.query_runner(committee_list, portfolio_list)
        # Add your processing logic here
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context


    def query_runner(self,committee_list, portfolio_list, *args, **kwargs):
        with transaction.atomic():
            preference = 1
            for committees, portfolios in zip(committee_list, portfolio_list):
                com = Committee.objects.get(pk=int(committees))
                prt = Portfolio.objects.get(pk=int(portfolios))

                self.get_student_and_school()

                # add to Total Global tracker
                a = AllTracker.objects.create(
                    student = self.current_student,
                    school = self.current_school,
                    challenge = "Sample",
                    committee = com.name,
                    portfolio = prt.name,
                    preference = preference,
                    team = "ASBFD",
                )
                a.save()

                preference += 1

                # create a unique Team Id
                 




class TeamView(FormView):
    template_name = "teams.html"
    form_class = TeamForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        # Process the form data here (save to database, send an email, etc.)
        members = self.request.POST.getlist('student')
        print(members)
        self.query_runner(members)
        # Add your processing logic here
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context


    def query_runner(self, team_members, *args, **kwargs):
        for member in team_members:
            # get team leader from user

            member_name = Students.objects.get(pk=member)

            # add all team members to
            a = AllTracker.objects.create(
                    student = member_name.name,
                    school = member_name.school.name,
                    challenge = "Sample",
                    team = "ASBFD",
            )
            a.save() 


class AddOnView(FormView):
    template_name = "add_ons.html"
    form_class = AddonForms
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        return super().form_valid(form)
