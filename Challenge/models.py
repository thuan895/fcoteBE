from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey
from Account.models import Account
from Assignment.models import Assignment
from Group.models import Group


class Challenge(models.Model):
    title = CharField(max_length=255, blank=True, null=True)
    description = TextField(blank=True, null=True)
    quality_assurance = BooleanField(default=False, blank=True, null=True)
    created_by = ForeignKey(
        Account, on_delete=models.CASCADE,  blank=True, null=True)
    image = CharField(blank=True, null=True, max_length=1000)
    group = ForeignKey(
        Group, on_delete=models.CASCADE,  blank=True, null=True)
    total_assignment = IntegerField(blank=True, null=True, default=0)
    start_at = DateTimeField(blank=True, null=True)
    end_at = DateTimeField(blank=True, null=True)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def dateEnd(seft):
        return seft.end_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def dateStart(seft):
        return seft.end_at.strftime("%Y-%m-%d %H:%M:%S")


class ChallengeElement(models.Model):
    challenge = ForeignKey(
        Challenge, on_delete=models.CASCADE,  blank=True, null=True)
    assignment = ForeignKey(
        Assignment, on_delete=models.CASCADE,  blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
