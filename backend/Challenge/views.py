from typing import Any, Dict

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import AddonForms, PreferenceForm, TeamForm

# Create your views here.


class CommitteeView(FormView):
    template_name = "preferences.html"
    form_class = PreferenceForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        # Process the form data here (save to database, send an email, etc.)
        name = form.cleaned_data["name"]
        # Add your processing logic here
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context


class TeamView(FormView):
    template_name = "teams.html"
    form_class = TeamForm
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        # Process the form data here (save to database, send an email, etc.)
        name = form.cleaned_data["name"]
        # Add your processing logic here
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context


class AddOnView(FormView):
    template_name = "add_ons.html"
    form_class = AddonForms
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        return super().form_valid(form)
