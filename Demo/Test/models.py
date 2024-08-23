from django.db import models

class Name(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class UserAccount(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.ForeignKey(Name, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)  # Add this line


    # name = models.OneToOneField(Name, on_delete=models.CASCADE)
