from django.contrib import admin
from .models import *
# Register your models here.


class AssignmentLanguageInline(admin.TabularInline):
    model = AssignmentLanguage


class ParammeterLanguageInline(admin.TabularInline):
    model = Parammeter


class TestCaseElementInline(admin.TabularInline):
    model = TestCaseElement


class TestCaseInline(admin.TabularInline):
    model = TestCase
    inlines = [TestCaseElementInline]


class TestCaseAdmin(admin.ModelAdmin):
    pass
    inlines = [TestCaseElementInline, ]


class AssignmentAdmin(admin.ModelAdmin):
    pass
    inlines = [AssignmentLanguageInline,
               ParammeterLanguageInline, TestCaseInline]


# admin.site.register(AssignmentTag)
admin.site.register(Language)
admin.site.register(Assignment, AssignmentAdmin)
# admin.site.register(AssignmentLanguage)
# admin.site.register(ServerRun)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestCaseElement)
