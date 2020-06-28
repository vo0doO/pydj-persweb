from django.contrib import admin

# Register your models here.
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
