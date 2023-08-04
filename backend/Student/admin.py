import csv
import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse

from .models import School, Students

# Register your models here.


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    pass


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
            file_name = school.name.replace(" ", "_") + ".csv"
            csv_filepath = os.path.join(filepath, file_name)
            with open(csv_filepath, "r") as file:
                csvreader = csv.DictReader(file)
                for row in csvreader:
                    name = row.get("Name")
                    email = row.get("Email")
                    contact = row.get("Contact")
                    std = row.get("Class")
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
    current_student = Students.objects.get(email=email)
    current_user = User.objects.get(username=email)
    if not current_student and not current_user:
        with transaction.atomic():
            s = Students.objects.create(
                name=name, email=email, contact=contact, standard=std, school=school
            )
            u = User.objects.create(username=email, password=create_password())
            s.save()
            u.save()
