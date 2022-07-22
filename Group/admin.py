from django.contrib import admin

from Challenge.models import Challenge
from .models import *
# Register your models here.


class GroupMemberInline(admin.TabularInline):
    model = GroupMember


class ChallengeInline(admin.TabularInline):
    model = Challenge


class GroupAdmin(admin.ModelAdmin):
    pass
    inlines = [ChallengeInline, GroupMemberInline, ]


admin.site.register(Group, GroupAdmin)
# admin.site.register(GroupMember)
