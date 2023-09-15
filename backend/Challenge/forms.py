from typing import Any, Dict

from django import forms

from Student.models import Students

from .models import Challenge, Committee, Portfolio


class ChallengeForm(forms.Form):
    challenge = forms.ModelChoiceField(
        queryset=Challenge.objects.all(), widget=forms.CheckboxSelectMultiple
    )


class PreferenceForm(forms.Form):
    committee = forms.ModelChoiceField(queryset=Committee.objects.all())
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all())

    def __init__(self, com_queryset=None, por_queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if com_queryset:
            self.fields["committee"].queryset = com_queryset

        if por_queryset:
            self.fields["portfolio"].queryset = por_queryset

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        committee = cleaned_data.get("committee")
        portfolio = cleaned_data.get("portfolio")

        if not committee or not portfolio:
            raise forms.ValidationError(
                "Both committee and portfolio must be selected."
            )


class TextForm(forms.Form):
    text = forms.TextInput()


class TeamForm(forms.Form):
    student1 = forms.ModelChoiceField(queryset=Students.objects.all())
    student2 = forms.ModelChoiceField(queryset=Students.objects.all())

    def __init__(self, queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if queryset:
            self.fields["student1"].queryset = queryset
            self.fields["student2"].queryset = queryset

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()

        student1 = cleaned_data.get("student1")
        student2 = cleaned_data.get("student2")

        if student1 and student2 and student1 == student2:
            raise forms.ValidationError(
                "Student 1 and Student 2 cannot be the same."
            )

        return cleaned_data


class ExtendedTeamForm(TeamForm):
    student3 = forms.ModelChoiceField(queryset=Students.objects.all())
    student4 = forms.ModelChoiceField(queryset=Students.objects.all())

    def __init__(self, queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if queryset:
            self.fields["student1"].queryset = queryset
            self.fields["student2"].queryset = queryset
            self.fields["student3"].queryset = queryset
            self.fields["student4"].queryset = queryset

    def clean(self):
        cleaned_data = super().clean()

        student1 = cleaned_data.get("student1")
        student2 = cleaned_data.get("student2")
        student3 = cleaned_data.get("student3")
        student4 = cleaned_data.get("student4")

        if student1 and student2 and student1 == student2:
            raise forms.ValidationError(
                "Student 1 and Student 2 cannot be the same."
            )
        if student1 and student3 and student1 == student3:
            raise forms.ValidationError(
                "Student 1 and Student 3 cannot be the same."
            )
        if student1 and student4 and student1 == student4:
            raise forms.ValidationError(
                "Student 1 and Student 4 cannot be the same."
            )

        if student2 and student3 and student2 == student3:
            raise forms.ValidationError(
                "Student 2 and Student 3 cannot be the same."
            )
        if student2 and student4 and student2 == student4:
            raise forms.ValidationError(
                "Student 2 and Student 4 cannot be the same."
            )

        if student3 and student4 and student3 == student4:
            raise forms.ValidationError(
                "Student 3 and Student 4 cannot be the same."
            )

        return cleaned_data


class PersonalInfoForm(forms.Form):
    text = text = forms.CharField(
        widget=forms.TextInput(attrs={"maxlength": 255})
    )
