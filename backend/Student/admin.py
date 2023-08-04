from django.contrib import admin
from django.contrib.auth.models import User
from .models import School, Students
from django.db import transaction

# Register your models here.


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass


def create_password()->str:
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
