from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey
from Account.models import Account
from Assignment.models import Assignment, Language
from Challenge.models import Challenge, ChallengeElement
from Group.models import Group


class Submit(models.Model):
    account = ForeignKey(
        Account, on_delete=models.CASCADE,  blank=True, null=True)
    challenge_element = ForeignKey(
        ChallengeElement, on_delete=models.CASCADE,  blank=True, null=True)
    source_code = TextField(blank=True, null=True)
    highest_score = IntegerField(blank=True, null=True, default=0)
    shortest_runtime = IntegerField(blank=True, null=True, default=0)
    language = ForeignKey(
        Language, on_delete=models.CASCADE,  blank=True, null=True)
    counter = IntegerField(blank=True, null=True, default=0)
    is_share = BooleanField(default=False, blank=True, null=True)
    completed_at = DateTimeField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.account.username+"-"+str(self.challenge_element)

    def dateUpdated(seft):
        return seft.updated_at.strftime("%Y-%m-%d %H:%M:%S")
