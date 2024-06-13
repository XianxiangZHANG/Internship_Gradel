# admin.py
from django.contrib import admin
from web import models

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model', 'object_id', 'timestamp', 'changes')
    list_filter = ('user', 'action', 'model', 'timestamp')

admin.site.register(models.Log, LogEntryAdmin)
