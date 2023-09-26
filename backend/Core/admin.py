import csv

from django.contrib import admin, messages
from django.http import HttpResponse
from django.db.models import Q

from .modelforms import ImpactModelAdminForm, MUNModelAdminForm
from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable


# Register your models here.
@admin.register(AllTracker)
class AllTrackerAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "school",
        "challenge",
        "committee",
        "portfolio",
        "preference",
    ]
    list_filter = ["school", "challenge", "committee", "portfolio"]
    actions = ["export_as_csv"]
    search_fields = ["student"]

    def export_as_csv(self, request, queryset):
        meta = (
            self.model._meta
        )  # used to determine the exported file name, The format is:app name. Model class name
        field_names = [field.name for field in meta.fields]  # all property names
        response = HttpResponse(
            content_type="text/csv"
        )  # specify the response content type
        response["content-disposition"] = f"attachment;filename={meta} .csv"
        response.charset = "utf-8-sig"
        writer = csv.writer(response)
        writer.writerow(field_names)  # write property names to csv
        for obj in queryset:  # traverse the list of objects to be exported
            row = writer.writerow(
                [getattr(obj, field) for field in field_names]
            )  # write the attribute values ​​of the current object to the csv
        return response

    export_as_csv.short_description = "Export csv"


@admin.register(ImpactChallengeTable)
class ImpactChallengeAdmin(admin.ModelAdmin):
    form = ImpactModelAdminForm
    list_display = [
        "student",
        "show_standard",
        "school",
        "get_preferences_one",
        "get_preferences_two",
        "committee",
        "portfolio",
        "remarks",
        "status",
    ]
    list_filter = ["school", "committee", "portfolio", "status"]
    list_editable = ("committee", "portfolio", "status")
    actions = ["export_as_csv"]

    def show_standard(self, obj):
        return obj.student.standard

    def save_model(self, request, obj, form, change):
        com = form.cleaned_data["committee"]
        por = form.cleaned_data["portfolio"]
        student = form.cleaned_data["id"].student

        q_filter = Q()
        q_filter &= Q(committee=com)
        q_filter &= Q(portfolio=por)
        q_filter &= Q(status="AL")
        q_filter &= ~Q(student=student)

        combination = ImpactChallengeTable.objects.filter(q_filter)

        if combination and len(combination) == 1:
            error_message = f"This committee and portfolio has already been alloted to \
                => {combination[0].student.name} from The School \
                => {combination[0].student.school.name}"  # noqa
            messages.set_level(request, messages.ERROR)
            messages.error(request, error_message)
        else:
            obj.save()

    def get_preferences(self, obj, preference):
        preferences = (
            AllTracker.objects.filter(
                student=obj.student,
                school=obj.school,
                challenge="MU20 Impact Challenge",
                preference=preference,
            )
            .values("committee", "portfolio")
            .first()
        )

        if preferences:
            return f"{preferences['committee']} {preferences['portfolio']}"
        return ""

    def get_preferences_one(self, obj):
        return self.get_preferences(obj, 1)

    def get_preferences_two(self, obj):
        return self.get_preferences(obj, 2)

    def export_as_csv(self, request, queryset):
        meta = (
            self.model._meta
        )  # used to determine the exported file name, The format is:app name. Model class name
        field_names = [field.name for field in meta.fields]  # all property names
        response = HttpResponse(
            content_type="text/csv"
        )  # specify the response content type
        response["content-disposition"] = f"attachment;filename={meta} .csv"
        response.charset = "utf-8-sig"  # Optional, modify the encoding to UTF-8 format with bom (excel will not have garbled characters)
        writer = csv.writer(response)
        writer.writerow(field_names)  # write property names to csv
        for obj in queryset:  # traverse the list of objects to be exported
            row = writer.writerow(
                [getattr(obj, field) for field in field_names]
            )  # write the attribute values ​​of the current object to the csv
        return response

    export_as_csv.short_description = "Export csv"
    get_preferences_one.short_description = "Preference 1"
    get_preferences_two.short_description = "Preference 2"
    show_standard.short_description = "Class"


@admin.register(MUNChallengeTable)
class MUNAdmin(admin.ModelAdmin):
    form = MUNModelAdminForm
    list_display = [
        "student",
        "show_standard",
        "school",
        "get_preferences_one",
        "get_preferences_two",
        "get_preferences_three",
        "committee",
        "portfolio",
        "remarks",
        "status",
    ]
    list_filter = ["school", "committee", "portfolio", "status"]
    list_editable = ("committee", "portfolio", "status")
    actions = ["export_as_csv"]

    def show_standard(self, obj):
        return obj.student.standard

    def save_model(self, request, obj, form, change):
        com = form.cleaned_data["committee"]
        por = form.cleaned_data["portfolio"]
        student = form.cleaned_data["id"].student

        q_filter = Q()
        q_filter &= Q(committee=com)
        q_filter &= Q(portfolio=por)
        q_filter &= Q(status="AL")
        q_filter &= ~Q(student=student)

        combination = MUNChallengeTable.objects.filter(q_filter)

        if combination and len(combination) == 1:
            error_message = f"This committee and portfolio has already been alloted to \
                => {combination[0].student.name} from The School \
                => {combination[0].student.school.name}"  # noqa
            messages.set_level(request, messages.ERROR)
            messages.error(request, error_message)
        else:
            print("This logic is working atleast")
            obj.save()

    def get_preferences(self, obj, preference):
        preferences = (
            AllTracker.objects.filter(
                student=obj.student,
                school=obj.school,
                challenge="Model United Nations",
                preference=preference,
            )
            .values("committee", "portfolio")
            .first()
        )

        if preferences:
            return f"{preferences['committee']} {preferences['portfolio']}"
        return ""

    def get_preferences_one(self, obj):
        return self.get_preferences(obj, 1)

    def get_preferences_two(self, obj):
        return self.get_preferences(obj, 2)

    def get_preferences_three(self, obj):
        return self.get_preferences(obj, 3)

    def export_as_csv(self, request, queryset):
        meta = (
            self.model._meta
        )  # used to determine the exported file name, The format is:app name. Model class name
        field_names = [field.name for field in meta.fields]  # all property names
        response = HttpResponse(
            content_type="text/csv"
        )  # specify the response content type
        response["content-disposition"] = f"attachment;filename={meta} .csv"
        response.charset = "utf-8-sig"  # Optional, modify the encoding to UTF-8 format with bom (excel will not have garbled characters)
        writer = csv.writer(response)
        writer.writerow(field_names)  # write property names to csv
        for obj in queryset:  # traverse the list of objects to be exported
            row = writer.writerow(
                [getattr(obj, field) for field in field_names]
            )  # write the attribute values ​​of the current object to the csv
        return response

    export_as_csv.short_description = "Export csv"
    get_preferences_one.short_description = "Preference 1"
    get_preferences_two.short_description = "Preference 2"
    get_preferences_three.short_description = "Preference 3"
    show_standard.short_description = "Class"
