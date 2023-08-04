from django.contrib import admin

from .models import Addon, Challenge, Committee, Portfolio

# Register your models here.


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    pass


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    pass


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass


@admin.register(Addon)
class AddOnAdmin(admin.ModelAdmin):
    pass
