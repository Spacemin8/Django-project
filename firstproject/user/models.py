from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    phone=models.CharField(max_length=10)
class verify(models.Model):
    email = models.EmailField(max_length=100, null=True)
    verification_code = models.CharField(max_length=10)
    expire_at = models.DateTimeField(null=True)
class Token(models.Model):
    accesstoken = models.CharField(max_length=100)
    refreshtoken = models.CharField(max_length=10)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)