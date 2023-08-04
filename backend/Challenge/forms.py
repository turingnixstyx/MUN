from django import forms

from Student.models import Students

from .models import Addon, Challenge, Committee, Portfolio


class ChallengeForm(forms.Form):
    challenge = forms.ModelChoiceField(queryset=Challenge.objects.all())


class PreferenceForm(forms.Form):
    committee = forms.ModelChoiceField(queryset=Committee.objects.all())
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all())


class AddonForms(forms.Form):
    add_on = forms.ModelMultipleChoiceField(
        queryset=Addon.objects.all(), widget=forms.CheckboxSelectMultiple
    )


class TextForm(forms.Form):
    text = forms.TextInput()


class TeamForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Students.objects.all())
