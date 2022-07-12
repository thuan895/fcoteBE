from django.db import models
from django.db.models.fields import CharField, DateTimeField, TextField, BooleanField, IntegerField
from django.db.models.fields.related import ForeignKey
from Account.models import Account


class Group(models.Model):
    title = CharField(max_length=255, blank=True, null=True)
    description = TextField(blank=True, null=True)
    join_code = CharField(max_length=10, blank=True, null=True)
    created_by = ForeignKey(
        Account, on_delete=models.CASCADE,  blank=True, null=True)
    image = CharField(blank=True, null=True, max_length=1000)
    total_member = IntegerField(blank=True, null=True, default=0)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title

class GroupMember(models.Model):
    group = ForeignKey(
        Group, on_delete=models.CASCADE,  blank=True, null=True)
    account = ForeignKey(
        Account, on_delete=models.CASCADE,  blank=True, null=True)
    total_completed = IntegerField(blank=True, null=True, default=0)
    total_missing = IntegerField(blank=True, null=True, default=0)
    total_score = IntegerField(blank=True, null=True, default=0)
    is_active = BooleanField(default=True, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = DateTimeField(auto_now=True, blank=True, null=True)
