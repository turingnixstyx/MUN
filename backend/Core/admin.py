from django.contrib import admin
from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable
import csv
from django.http import HttpResponse
from .modelforms import MUNModelAdminForm, ImpactModelAdminForm


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


@admin.register(ImpactChallengeTable)
class ImpactChallengeAdmin(admin.ModelAdmin):
    form=ImpactModelAdminForm
    list_display = ["student", "school", "committee", "portfolio", "remarks", 'get_preferences_one', 'get_preferences_two', 'get_preferences_three']
    list_filter = ["school", "committee", "portfolio"]
    list_editable = ('committee', 'portfolio',)
    actions = ["export_as_csv"]

    def get_preferences_one(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="Impact Challenge", preferences=1).values('committee', 'portfolio')
        pref_list = f"{preferences[0].get('committee')} {preferences[0].get('portfolio')}"
        return pref_list
    
    def get_preferences_two(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="Impact Challenge", preferences=2).values('committee', 'portfolio')
        pref_list = f"{preferences[0].get('committee')} {preferences[0].get('portfolio')}"
        return pref_list
    
    def get_preferences_three(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="Impact Challenge", preferences=3).values('committee', 'portfolio')
        pref_list = f"{preferences[0].get('committee')} {preferences[0].get('portfolio')}"
        return pref_list


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


@admin.register(MUNChallengeTable)
class MUNAdmin(admin.ModelAdmin):
    form=MUNModelAdminForm
    list_display = ["student", "school", "committee", "portfolio"]
    list_filter = ["school", "committee", "portfolio"]
    actions = ["export_as_csv"]

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
