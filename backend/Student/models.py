import os

from django.db import models

# Create your models here.


def upload_to(instance, filename):
    # Generate the upload path dynamically based on the instance's name
    filename, extension = os.path.splitext(filename)
    return f"csv_media/{instance.name}{extension}"


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    csv_file = models.FileField(upload_to=upload_to, null=True)

    def __str__(self):
        return self.name


class Students(models.Model):
    name = models.CharField(
        max_length=255, unique=False, null=True, blank=False, default="Test Name"
    )
    email = models.EmailField(
        max_length=254, unique=True, null=False, default="sample@email.com"
    )
    contact = models.CharField(
        max_length=25, unique=False, null=True, default="1111111111", blank=True
    )
    standard = models.CharField(max_length=255, unique=False, blank=True, null=True)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="school_student",
        unique=False,
        null=True,
    )
    team = models.CharField(max_length=5, unique=False, null=True, blank=True)
    password = models.CharField(
        max_length=100, unique=False, null=False, blank=False, default="password"
    )

    personal_info = models.TextField(null=True)

    def __str__(self):
        return f"{self.name} {self.email}"
