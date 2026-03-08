from django.contrib import admin
from .models import Subject, Video, PastPaper


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subject', 'level', 'uploaded_at']
    list_filter = ['level', 'subject']
    search_fields = ['title', 'subject__name']


@admin.register(PastPaper)
class PastPaperAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subject', 'level', 'uploaded_at']
    list_filter = ['level', 'subject']
    search_fields = ['title', 'subject__name']