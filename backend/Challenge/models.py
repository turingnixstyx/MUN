from django.db import models

# Create your models here.


class Challenge(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Addon(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
