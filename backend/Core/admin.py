from django.contrib import admin
from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable

# Register your models here.
@admin.register(AllTracker)
class AllTrackerAdmin(admin.ModelAdmin):
    pass


@admin.register(ImpactChallengeTable)
class ImpactChallengeAdmin(admin.ModelAdmin):
    pass


@admin.register(MUNChallengeTable)
class MUNAdmin(admin.ModelAdmin):
    pass