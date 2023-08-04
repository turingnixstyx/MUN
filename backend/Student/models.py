from django.db import models

# Create your models here.



class School(models.Model):
    name = models.CharField(max_length=255, unique=True)


    def __str__(self):
        return self.name




class Students(models.Model):
    name = models.CharField(max_length=255, unique=False, null=False, default="Test Name")
    email = models.EmailField(max_length=254, unique=True, null=False, default="sample@email.com")
    contact = models.CharField(max_length=10, unique=False, null=False, default="1111111111")
    standard = models.IntegerField(default=10)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_student", unique=False, null=True)


    def __str__(self):
        return f"{self.name} {self.email}"
