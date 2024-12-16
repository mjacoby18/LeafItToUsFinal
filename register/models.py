from django.db import models

class User(models.Model):
    username=models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password1=models.CharField(max_length=50)
    password2=models.CharField(max_length=50)