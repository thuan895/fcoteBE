from django.contrib import admin
from .models import *
# Register your models here.


class ChallengeElementInline(admin.TabularInline):
    model = ChallengeElement


class ChallengeAdmin(admin.ModelAdmin):
    pass
    inlines = [ChallengeElementInline]


admin.site.register(Challenge, ChallengeAdmin)
# admin.site.register(ChallengeElement)
