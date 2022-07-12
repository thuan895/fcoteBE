
from django.db import models
from utils.constants.models import Gender
from django.db.models.fields import CharField, DateTimeField, TextField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey


class Organization(models.Model):
    title = CharField(max_length=255, blank=True, null=True)
    address = TextField(blank=True, null=True)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Account(models.Model):
    username = CharField(unique=True, blank=True, null=True, max_length=255)
    email = CharField(blank=True, null=True, max_length=255)
    token = CharField(blank=True, null=True, max_length=1000)
    first_name = CharField(blank=True, null=True, max_length=255)
    last_name = CharField(blank=True, null=True, max_length=255)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.username

    def fullname(self):
        return self.first_name + " "+self.last_name


class Profile(models.Model):
    account = ForeignKey(Account, on_delete=models.CASCADE,
                         blank=True, null=True)
    avatar = CharField(blank=True, null=True, max_length=1000)
    phone = CharField(blank=True, null=True, max_length=255)
    birthday = CharField(blank=True, null=True, max_length=255)
    gender = models.IntegerField(blank=True, null=True, choices=Gender.choices)
    organization = ForeignKey(
        Organization, on_delete=models.CASCADE, blank=True, null=True)
    total_assigment = IntegerField(blank=True, null=True, default=0)
    total_challenge = IntegerField(blank=True, null=True, default=0)
    total_group = IntegerField(blank=True, null=True, default=0)
    total_score = IntegerField(blank=True, null=True, default=0)
    assignment_easy = IntegerField(blank=True, null=True, default=0)
    assignment_medium = IntegerField(blank=True, null=True, default=0)
    assignment_hard = IntegerField(blank=True, null=True, default=0)
    city = CharField(blank=True, null=True, max_length=255)
    country = CharField(blank=True, null=True, max_length=255)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.account.username
