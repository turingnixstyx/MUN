from django.db import models
from django.utils import timezone

from Challenge.models import Committee, Portfolio


# Create your models here.
class AllTracker(models.Model):
    student = models.CharField(max_length=255, unique=False, null=True, blank=True)
    school = models.CharField(max_length=255)
    challenge = models.CharField(max_length=255, unique=False, null=True, blank=True)
    committee = models.CharField(max_length=255, unique=False, null=True, blank=True)
    portfolio = models.CharField(max_length=255, unique=False, null=True, blank=True)
    add_on = models.CharField(max_length=255, unique=False, null=True, blank=True)
    team = models.CharField(max_length=100, unique=False, null=True, blank=True)
    preference = models.IntegerField(unique=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField()

    def __str__(self):
        return self.student + " " + self.school


class ImpactChallengeTable(models.Model):
    STATUS_CHOICES = (
        ("NF", "Not filled"),
        ("AW", "Awaiting"),
        ("AL", "Alloted"),
    )
    student = models.CharField(max_length=255, unique=True, null=True, blank=True)
    school = models.CharField(max_length=255)
    committee = models.ForeignKey(
        Committee, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="NF")
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    remarks = models.TextField()

    def __str__(self):
        return "IC " + self.student + " " + self.school


class MUNChallengeTable(models.Model):
    STATUS_CHOICES = (
        ("NF", "Not filled"),
        ("AW", "Awaiting"),
        ("AL", "Alloted"),
    )
    student = models.CharField(max_length=255, unique=True, null=True, blank=True)
    school = models.CharField(max_length=255)
    committee = models.ForeignKey(
        Committee, on_delete=models.CASCADE, null=True, blank=True
    )
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="NF")
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    remarks = models.TextField()

    def __str__(self):
        return "MUN " + self.student + " " + self.school
