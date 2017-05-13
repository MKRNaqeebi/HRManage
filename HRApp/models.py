from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class UserType(models.Model):
    user_type = models.CharField(max_length=3, default='A')
    user = models.ForeignKey(User)


class Category(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField(default='this is category disc')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Company (models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    location = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    category = models.ForeignKey(Category)
    company = models.ForeignKey(Company)
    location = models.CharField(max_length=128)
    salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Apply(models.Model):
    description = models.TextField()
    document = models.FileField(upload_to='media')
    job = models.ForeignKey(Job)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class RateApply(models.Model):
    rate = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    comment = models.TextField()
    sme = models.ForeignKey(settings.AUTH_USER_MODEL)
    apply = models.ForeignKey(Apply)


class InterviewCall(models.Model):
    apply = models.ForeignKey(Apply)
