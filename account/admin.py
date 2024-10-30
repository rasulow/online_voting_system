from django.contrib import admin
from unfold.admin import ModelAdmin
from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'is_active', 'formatted_created_at', 'formatted_updated_at')
    search_fields = ('username',)
    list_filter = ('user_type', 'created_at')
    
    
@admin.register(models.Passport)
class PassportAdmin(ModelAdmin):
    list_display = ('passport_id', 'get_full_name', 'get_age', 'gender', 'judicial', 'formatted_created_at', 'formatted_updated_at')
    search_fields = ('passport_id', 'first_name', 'last_name')
    list_filter = ('judicial', 'created_at')