
from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey
from utils.constants.models import DataType,  Difficulty, InOutType, RunOnServerType
from Account.models import Account


class AssignmentTag(models.Model):
    title = CharField(max_length=255, blank=True, null=True)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Language(models.Model):
    title = CharField(max_length=255, blank=True, null=True)
    is_active = BooleanField(default=True, blank=True, null=True)
    code = CharField(max_length=255, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class Assignment(models.Model):
    title = CharField(blank=True, null=True, max_length=255)
    description = TextField(blank=True, null=True)
    sample = TextField(blank=True, null=True)
    image = CharField(blank=True, null=True, max_length=1000)
    difficulty = IntegerField(
        blank=True, null=True, choices=Difficulty.choices)
    total_test_case = IntegerField(blank=True, null=True, default=0)
    score = IntegerField(blank=True, null=True, default=0)
    assignment_tag = ForeignKey(
        AssignmentTag, on_delete=models.CASCADE, blank=True, null=True)
    quality_assurance = BooleanField(default=False, blank=True, null=True)
    character_limit = IntegerField(blank=True, null=True, default=10000)
    total_participant = IntegerField(blank=True, null=True, default=0)
    created_by = ForeignKey(
        Account, on_delete=models.CASCADE,  blank=True, null=True)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def date(seft):
        return seft.created_at.strftime("%Y-%m-%d %H:%M:%S")


class AssignmentLanguage(models.Model):
    assignment = ForeignKey(
        Assignment, on_delete=models.CASCADE,  blank=True, null=True)
    language = ForeignKey(
        Language, on_delete=models.CASCADE,  blank=True, null=True)
    time_limit = IntegerField(blank=True, null=True, default=10000)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.assignment.title


class Parammeter(models.Model):
    assignment = ForeignKey(
        Assignment, on_delete=models.CASCADE,  blank=True, null=True)
    order = IntegerField(blank=True, null=True)
    type = IntegerField(
        blank=True, null=True, choices=InOutType.choices)
    name = CharField(blank=True, null=True, max_length=254)
    data_type = IntegerField(
        blank=True, null=True, choices=DataType.choices)
    description = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.assignment.title


class TestCase(models.Model):
    assignment = ForeignKey(
        Assignment, on_delete=models.CASCADE,  blank=True, null=True)
    order = IntegerField(blank=True, null=True)
    is_private = BooleanField(blank=True, null=True, default=False)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.assignment.title + "-"+str(self.order)


class TestCaseElement(models.Model):
    test_case = ForeignKey(
        TestCase, on_delete=models.CASCADE,  blank=True, null=True)
    type = IntegerField(blank=True, null=True, choices=InOutType.choices)
    order = IntegerField(blank=True, null=True)
    data_type = IntegerField(blank=True, null=True, choices=DataType.choices)
    value = TextField(blank=True, null=True)

    def __str__(self):
        return str(self.test_case.id)+"."+str(self.type) + "."+str(self.order) + "."+self.value


# class ServerRun(models.Model):
#     server = IntegerField(
#         blank=True, null=True, choices=RunOnServerType.choices)
#     updated_at = DateTimeField(auto_now=True, blank=True, null=True)
