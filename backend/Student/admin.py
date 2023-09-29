from django.contrib import admin
from django.contrib.auth.models import User

from .models import School, Students

from .admin_actions import CSVExport, StudentImporter, TeamFilter


class BaseAdminClass(admin.ModelAdmin):
    actions = ['export_select_as_csv']

    def export_selected_as_csv(self, request, queryset):
        return CSVExport.export_as_csv(self, request, queryset)

    export_selected_as_csv.short_description = "Export csv"


@admin.register(Students)
class StudentAdmin(BaseAdminClass):
    list_display = ["name", "standard", "school"]
    list_filter = ["standard", "school", TeamFilter]
    search_fields = ["name", "contact", "email"]
    actions = BaseAdminClass.actions + ["delete_users_from_students", "set_team_value_to_zero"] # type: ignore

    def delete_users_from_students(self, request, queryset):
        for student in queryset:
            email = student.email
            linked_user = User.objects.filter(username=email)

            if linked_user and len(linked_user) == 1:
                linked_user.delete()
                print(f"{student.name} deleted successfully!")
            else:
                print("User not found!")

    def set_team_value_to_zero(self, request, queryset):
        for student in queryset:
            if student.team is not None:
                student.team = None
                student.save()

    delete_users_from_students.short_description = "Delete Student <--> USER"
    set_team_value_to_zero.short_description = "Team 0"


@admin.register(School)
class SchoolAdmin(BaseAdminClass):
    actions = BaseAdminClass.actions + [
        "import_students_from_csv",
    ]  # type: ignore

    def import_students_from_csv(self, request, queryset):
        # Using the import_students_from_csv method from StudentImporter
        return StudentImporter.import_students_from_csv(request, queryset)

    import_students_from_csv.short_description = "Import Students"
