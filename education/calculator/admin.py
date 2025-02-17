from django.contrib import admin
from .models import MathEntry

@admin.register(MathEntry)
class MathEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'content')