from django.contrib import admin
from .models import Task

# Register your models here.


class AdminTask(admin.ModelAdmin):
    list_display = ("author", "is_complete", "title", "id")
    list_filter = ("author", "is_complete")


admin.site.register(Task, AdminTask)
