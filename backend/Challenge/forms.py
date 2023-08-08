from typing import Any, Dict

from django import forms

from Student.models import Students

from .models import Addon, Challenge, Committee, Portfolio


class ChallengeForm(forms.Form):
    challenge = forms.ModelChoiceField(queryset=Challenge.objects.all(), widget=forms.CheckboxSelectMultiple)


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
    student1 = forms.ModelChoiceField(queryset=Students.objects.all())
    student2 = forms.ModelChoiceField(queryset=Students.objects.all())
    student3 = forms.ModelChoiceField(queryset=Students.objects.all())

    def __init__(self, queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if queryset:
            self.fields["student1"].queryset = queryset
            self.fields["student2"].queryset = queryset
            self.fields["student3"].queryset = queryset

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        student1 = cleaned_data.get("student1")
        student2 = cleaned_data.get("student2")
        student3 = cleaned_data.get("student3")

        if student1 and student2 and student1 == student2:
            raise forms.ValidationError("Student 1 and Student 2 cannot be the same.")
        if student1 and student3 and student1 == student3:
            raise forms.ValidationError("Student 1 and Student 3 cannot be the same.")
        if student2 and student3 and student2 == student3:
            raise forms.ValidationError("Student 2 and Student 3 cannot be the same.")

        return cleaned_data
