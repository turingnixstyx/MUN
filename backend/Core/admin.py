from django.contrib import admin
from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable

# Register your models here.
@admin.register(AllTracker)
class AllTrackerAdmin(admin.ModelAdmin):
    list_display = ['student', 'school', 'challenge', 'committee', 'portfolio', 'preference']
    list_filter = ['school', 'challenge', 'committee', 'portfolio']


@admin.register(ImpactChallengeTable)
class ImpactChallengeAdmin(admin.ModelAdmin):
    list_display = ['student', 'school', 'committee', 'portfolio']
    list_filter = ['school', 'committee', 'portfolio']



@admin.register(MUNChallengeTable)
class MUNAdmin(admin.ModelAdmin):
    list_display = ['student', 'school', 'committee', 'portfolio']
    list_filter = ['school', 'committee', 'portfolio']