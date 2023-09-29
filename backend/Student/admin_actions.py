from django.contrib import admin
from typing import Any
from django.http import HttpResponse
import csv
import random
from django.conf import settings
import os

from Core.models import AllTracker, MUNChallengeTable
from .models import School, Students
from django.db import transaction
from django.contrib.auth.models import User


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


class CSVExport:

    @staticmethod
    def export_as_csv(model_admin, request, queryset):
        meta = model_admin.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type="text/csv")
        response["content-disposition"] = f"attachment;filename={meta}.csv"
        response.charset = "utf-8-sig"
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response


class StudentImporter:
    @staticmethod
    def create_password(school_name: str, student_name: str) -> str:
        try:
            uiq = str(random.randint(100, 10000))

            school_name = school_name.replace(" ", "").upper().strip()
            student_name = student_name.replace(" ", "").strip()

            password = f"MU{student_name}@{school_name}{uiq}".replace(" ", "")

        except Exception as e:
            print(str(e))
            password = "password"
        return password

    @staticmethod
    def create_students_as_users(name: str, email: str, contact: str, std: str, school: str, plist: list) -> None:
        print(f"name {name} email {email} contact {contact} std {std} school {school} plist {plist}")
        current_student = Students.objects.filter(email=email)
        current_user = User.objects.filter(username=email)
        my_pass = StudentImporter.create_password(school_name=school, student_name=name)
        if not current_student and not current_user:
            with transaction.atomic():
                student = Students.objects.create(
                    name=name,
                    email=email,
                    contact=contact,
                    standard=std,
                    school=School.objects.get(name=school),
                    password=my_pass,
                )
                student.save()
                user = User.objects.create_user(
                    username=email, password=my_pass
                )
                user.save()

                if plist:
                    for pref in plist:
                        com = pref.get('com')
                        prt = pref.get('portfolio')
                        per = pref.get('preference')
                        a = AllTracker()

                        if com and prt and per:
                            a = AllTracker.objects.create(
                                student=str(name),
                                school=str(school),
                                challenge=str("Model United Nations"),
                                committee=str(com),
                                portfolio=str(prt),
                                preference=int(per),
                                team=school,
                            )

                            a.save()
                    
                    t = MUNChallengeTable.objects.create(
                        student=student,
                        school=School.objects.get(name=school),
                        all_tracker=a,
                    )

                    t.save()

    @staticmethod
    def import_students_from_csv(request, queryset):
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
                    name = email = contact = std = ""
                    preference_list = []
                    d1, d2, d3 = {}, {}, {}
                    for field in field_names:
                        if "name" in field.lower():
                            name = row.get(field, "").strip()
                        elif "mail" in field.lower():
                            email = row.get(field, "").strip().replace(" ", "")
                        elif "contact" in field.lower():
                            contact = row.get(field, "").strip()
                        elif "class" in field.lower() or "grade" in field.lower() or "standard" in field.lower():
                            std = row.get(field, "").strip()

                        if "Committee" in field:
                            if "1" in field:
                                d1 = {"com": row.get(field), "preference": 1, "portfolio": ""}
                            if "2" in field:
                                d2 = {"com": row.get(field), "preference": 2, "portfolio": ""}
                            if "3" in field:
                                d3 = {"com": row.get(field), "preference": 3, "portfolio": ""}
                        elif "Portfolio" in field:
                            if "1" in field and d1.get("com", None) and d1.get("preference", -1) == 1:
                                d1["portfolio"] = row.get(field)
                            if "2" in field and d2.get("com", None) and d2.get("preference", -1) == 2:
                                d2["portfolio"] = row.get(field)
                            if "3" in field and d3.get("com", None) and d3.get("preference", -1) == 3:
                                d3["portfolio"] = row.get(field)

                    if d1 and d2 and d3:
                        preference_list = [d1, d2, d3]
                    school_name = school.name
                    StudentImporter.create_students_as_users(
                        name=name,
                        email=email,
                        contact=contact,
                        std=std,
                        school=school_name,
                        plist=preference_list
                    )
