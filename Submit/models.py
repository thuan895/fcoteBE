from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey
from Account.models import Account
from Assignment.models import Assignment, Language
from Challenge.models import Challenge
from Group.models import Group


class Submit(models.Model):
    account = ForeignKey(
        Account, on_delete=models.CASCADE,  blank=True, null=True)
    challenge = ForeignKey(
        Challenge, on_delete=models.CASCADE,  blank=True, null=True)
    assignment = ForeignKey(
        Assignment, on_delete=models.CASCADE,  blank=True, null=True)
    source_code = TextField(blank=True, null=True)
    highest_score = IntegerField(blank=True, null=True, default=0)
    language = ForeignKey(
        Language, on_delete=models.CASCADE,  blank=True, null=True)
    is_share = BooleanField(default=False, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title


class SubmitResult(models.Model):
    submit = ForeignKey(
        Submit, on_delete=models.CASCADE,  blank=True, null=True)
    runtime = IntegerField(blank=True, null=True, default=0)
    passed = IntegerField(blank=True, null=True, default=0)
    failure = IntegerField(blank=True, null=True, default=0)
    score = IntegerField(blank=True, null=True, default=0)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
