from django.contrib import admin
from .models import (
    PaperProgress,
    PastPaper,
    StudentProfile,
    Subject,
    Video,
    VideoProgress,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "subject", "level", "uploaded_at"]
    list_filter = ["level", "subject"]
    search_fields = ["title", "subject__name"]


@admin.register(PastPaper)
class PastPaperAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "subject", "level", "uploaded_at"]
    list_filter = ["level", "subject"]
    search_fields = ["title", "subject__name"]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "joined_at"]
    search_fields = ["user__username", "user__email"]


@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "video", "completed", "watched_at"]
    list_filter = ["completed", "video__subject", "video__level"]
    search_fields = ["student__username", "video__title"]


@admin.register(PaperProgress)
class PaperProgressAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "paper", "viewed", "viewed_at"]
    list_filter = ["viewed", "paper__subject", "paper__level"]
    search_fields = ["student__username", "paper__title"]