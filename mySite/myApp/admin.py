from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Suggestion_Model)
admin.site.register(models.Comment_Model)