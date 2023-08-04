from django.contrib import admin

from .models import School, Students

# Register your models here.


@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    pass
