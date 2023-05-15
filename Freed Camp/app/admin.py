from django.contrib import admin

# Register your models here.
from app import models

admin.site.register(models.Create)
admin.site.register(models.Projects)
admin.site.register(models.Add_Lists)
admin.site.register(models.Tasks)
