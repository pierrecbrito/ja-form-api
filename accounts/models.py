from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission

class Role(models.Model):
    name  = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class User(AbstractBaseUser):
    name  = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    role =  models.ForeignKey(Role, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class User_Role_Permissions(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)