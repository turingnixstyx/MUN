import csv
import os
from typing import Any, Optional

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.query import QuerySet
from django.http import HttpResponse

from .models import School, Students

# Register your models here.


class TeamFilter(admin.SimpleListFilter):
    title = "engagment"
    parameter_name = "has_teams"

    def lookups(self, request, model_admin):
        return (
            ("yes", "With Teams"),
            ("no", "Without Teams"),
        )

    def queryset(self, request: Any, queryset):
        if self.value() == "yes":
            return queryset.exclude(team__isnull=True)
        if self.value() == "no":
            return queryset.exclude(team__isnull=False)


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "standard", "school"]
    list_filter = ["standard", "school", TeamFilter]
    search_fields = ["name", "contact", "email"]
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


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    actions = [
        "export_as_csv",
        "import_students_from_csv",
    ]  # add actions, Corresponding method name

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

    def import_students_from_csv(self, request, queryset):
        filepath = os.path.join(settings.BASE_DIR, "Media/csv_media")

        for school in queryset:
            file_name = (
                school.name.replace(" ", "_") if " " in school.name else school.name
            )
            file_name = str(file_name) + ".csv"
            csv_filepath = os.path.join(filepath, file_name)
            with open(csv_filepath, "r") as file:
                csvreader = csv.DictReader(file)
                field_names = csvreader.fieldnames

                print(field_names)
                for row in csvreader:
                    for field in field_names:
                        if "name" in field.lower():
                            name = row.get(field)
                        elif "email" in field.lower():
                            email = row.get(field)

                        elif "contact" in field.lower():
                            contact = row.get(field)

                        if "class" in field.lower():
                            temp = row.get(field)
                            kclass = "".join(
                                filter(lambda char: not char.isalpha(), temp)
                            )
                            std = int(kclass)

                    school_name = school.name
                    create_students_as_users(
                        name=name,
                        email=email,
                        contact=contact,
                        std=std,
                        school=school_name,
                    )

    export_as_csv.short_description = "Export csv"
    import_students_from_csv.short_description = "Import Students"


def create_password() -> str:
    return "password"


def create_students_as_users(
    name: str, email: str, contact: str, std: str, school: str
) -> None:
    print(f"name {name} email {email} contact {contact} ")
    current_student = Students.objects.filter(email=email)
    current_user = User.objects.filter(username=email)
    if not current_student and not current_user:
        with transaction.atomic():
            s = Students.objects.create(
                name=name,
                email=email,
                contact=contact,
                standard=std,
                school=School.objects.get(name=school),
            )
            s.save()
            u = User.objects.create(username=email, password=create_password())
            u.save()
