import csv
import os
import random
from typing import Any

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
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
    actions = ["export_as_csv", "delete_users_from_students"]

    def export_as_csv(self, request, queryset):
        meta = (
            self.model._meta
        )
        # used to determine the exported file name,
        # The format is:app name. Model class name
        field_names = [
            field.name for field in meta.fields
        ]  # all property names
        response = HttpResponse(
            content_type="text/csv"
        )  # specify the response content type
        response["content-disposition"] = f"attachment;filename={meta} .csv"
        response.charset = "utf-8-sig"
        writer = csv.writer(response)
        writer.writerow(field_names)  # write property names to csv
        for obj in queryset:  # traverse the list of objects to be exported
            row = writer.writerow( # noqa
                [getattr(obj, field) for field in field_names]
            )  # write the attribute values ​​of the current object to the csv
        return response

    def delete_users_from_students(self, request, queryset):
        for student in queryset:
            email = student.email
            linked_user = User.objects.filter(username=email)

            if linked_user and len(linked_user) == 1:
                linked_user.delete()
                print(f"{student.name} deleted successfully!")
            else:
                print("User not found!")

    export_as_csv.short_description = "Export csv"
    delete_users_from_students.short_description = "Delete Student <--> USER"


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    actions = [
        "export_as_csv",
        "import_students_from_csv",
    ]  # add actions, Corresponding method name

    def export_as_csv(self, request, queryset):
        meta = (
            self.model._meta
        )
        field_names = [
            field.name for field in meta.fields
        ]  # all property names
        response = HttpResponse(
            content_type="text/csv"
        )  # specify the response content type
        response["content-disposition"] = f"attachment;filename={meta} .csv"
        response.charset = "utf-8-sig"
        writer = csv.writer(response)
        writer.writerow(field_names)  # write property names to csv
        for obj in queryset:  # traverse the list of objects to be exported
            row = writer.writerow( # noqa
                [getattr(obj, field) for field in field_names]
            )  # write the attribute values ​​of the current object to the csv
        return response

    def import_students_from_csv(self, request, queryset):
        filepath = os.path.join(settings.BASE_DIR, "Media/csv_media")

        for school in queryset:
            csv_file_name = School.objects.get(name=school.name).csv_file
            file_name = str(csv_file_name).split("/")[1]
            csv_filepath = os.path.join(filepath, file_name)
            with open(csv_filepath, "r") as file:
                csvreader = csv.DictReader(file)
                field_names = csvreader.fieldnames

                print(field_names)
                for row in csvreader:
                    for field in field_names:
                        if "name" in field.lower():
                            name = row.get(field, None)
                            if name:
                                name = name.strip()
                        elif "email" in field.lower():
                            email = row.get(field, None)
                            if email:
                                email = email.strip()
                                if " " in email:
                                    email = email.replace(" ", "")

                        elif "contact" in field.lower():
                            contact = row.get(field, None)
                            if contact:
                                contact = contact.strip()

                        if (  # noqa
                            "class" in field.lower()
                            or "grade" in field.lower()
                            or "standard" in field.lower()
                        ):
                            std = row.get(field, None)
                            if std:
                                std = std.strip()

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


def create_password(school_name: str, student_name: str) -> str:
    try:
        uiq = str(random.randint(100, 10000))

        if " " in school_name:
            school_name.replace(" ", "").upper().strip()
        if " " in student_name:
            student_name.replace(" ", "").strip()

        password = f"MU{student_name}@{school_name}{str(uiq)}".replace(" ", "")

    except Exception as e:
        print(str(e))
        password = "password"
    return password


def create_students_as_users(
    name: str, email: str, contact: str, std: str, school: str
) -> None:
    print(f"name {name} email {email} contact {contact} ")
    current_student = Students.objects.filter(email=email)
    current_user = User.objects.filter(username=email)
    my_pass = create_password(school_name=school, student_name=name)
    if not current_student and not current_user:
        with transaction.atomic():
            s = Students.objects.create(
                name=name,
                email=email,
                contact=contact,
                standard=std,
                school=School.objects.get(name=school),
                password=my_pass,
            )
            s.save()
            u = User.objects.create(
                username=email, password=make_password(my_pass)
            )
            u.save()
