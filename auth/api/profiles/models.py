from django.db import models

from users.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Se cambio el FK

    first_name = models.CharField(max_length=20, null=False, blank=False)
    middle_name = models.CharField(max_length=20)
    first_surname = models.CharField(max_length=20, null=False, blank=False)
    second_surname = models.CharField(max_length=20)

    birth_date = models.DateField(null=False, blank=False)
    age = models.IntegerField(default = 0) 
    place_of_birth = models.CharField(max_length=30, null=False, blank=False)
    residence_place = models.CharField(max_length=30, null=False, blank=False)
    residence_country = models.CharField(max_length=30, null=False, blank=False)

    status_delete = models.BooleanField(default=False)
