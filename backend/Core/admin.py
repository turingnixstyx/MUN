from django.contrib import admin
from django import forms
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
    list_display = ["student", "school", 'get_preferences_one', 'get_preferences_two', "committee", "portfolio", "remarks", "status"]
    list_filter = ["school", "committee", "portfolio", "status"]
    list_editable = ('committee', 'portfolio', "status")
    actions = ["export_as_csv"]

    def save_model(self, request, obj, form, change):
        com = form.cleaned_data['committee']
        por = form.cleaned_data['portfolio']

        combination = ImpactChallengeTable.objects.filter(committee=com, portfolio=por)
        if combination:
            error_message = 'This combination of committee and portfolio is already allotted'
            form.add_error(None, forms.ValidationError(error_message))
        else:
            print("This logic is working atleast")
        
        obj.save()



    def get_preferences_one(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="Impact Challenge", preference=1).values('committee', 'portfolio')
        pref_list = f"{preferences[0].get('committee')} {preferences[0].get('portfolio')}"
        return pref_list
    
    def get_preferences_two(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="Impact Challenge", preference=2).values('committee', 'portfolio')
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


@admin.register(MUNChallengeTable)
class MUNAdmin(admin.ModelAdmin):
    form=MUNModelAdminForm
    list_display = ["student", "school", 'get_preferences_one', 'get_preferences_two', 'get_preferences_three', "committee", "portfolio", "remarks", 'status']
    list_filter = ["school", "committee", "portfolio", "status"]
    list_editable = ('committee', 'portfolio', 'status')
    actions = ["export_as_csv"]

    def save_model(self, request, obj, form, change):
        com = form.cleaned_data['committee']
        por = form.cleaned_data['portfolio']

        combination = MUNChallengeTable.objects.filter(committee=com, portfolio=por)
        if combination:
            error_message = 'This combination of committee and portfolio is already allotted'
            form.add_error(None, forms.ValidationError(error_message))
        else:
            print("This logic is working atleast")
        
        obj.save()

    def get_preferences_one(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="United Nations Simulation", preference=1).values('committee', 'portfolio')
        pref_list = f"{preferences[0].get('committee')} {preferences[0].get('portfolio')}"
        return pref_list
    
    def get_preferences_two(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="United Nations Simulation", preference=2).values('committee', 'portfolio')
        pref_list = f"{preferences[0].get('committee')} {preferences[0].get('portfolio')}"
        return pref_list
    
    def get_preferences_three(self, obj):
        preferences = AllTracker.objects.filter(student=obj.student, school=obj.school, challenge="United Nations Simulation", preference=3).values('committee', 'portfolio')
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
