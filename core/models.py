from django.db import models
from django.contrib.auth.models import User


def video_upload_path(instance, filename):
    subject_name = instance.subject.name if instance.subject else "unknown_subject"
    level = instance.level if getattr(instance, "level", None) else "L2"
    return f"videos/{subject_name}/{level}/{filename}"


def paper_upload_path(instance, filename):
    subject_name = instance.subject.name if instance.subject else "unknown_subject"
    level = instance.level if getattr(instance, "level", None) else "L2"
    return f"past_papers/{subject_name}/{level}/{filename}"


class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    LEVEL_CHOICES = [
        ("L2", "Level 2"),
        ("L3", "Level 3"),
        ("L4", "Level 4"),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default="L2")
    video_file = models.FileField(upload_to=video_upload_path, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.level})"


class PastPaper(models.Model):
    LEVEL_CHOICES = [
        ("L2", "Level 2"),
        ("L3", "Level 3"),
        ("L4", "Level 4"),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="past_papers")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default="L2")
    paper_file = models.FileField(upload_to=paper_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.level})"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class VideoProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="video_progress")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="progress_records")
    completed = models.BooleanField(default=False)
    watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "video")
        ordering = ["-watched_at"]

    def __str__(self):
        return f"{self.student.username} - {self.video.title}"


class PaperProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paper_progress")
    paper = models.ForeignKey(PastPaper, on_delete=models.CASCADE, related_name="progress_records")
    viewed = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "paper")
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.student.username} - {self.paper.title}"


def study_material_upload_path(instance, filename):
    subject_name = instance.subject.name if instance.subject else "unknown_subject"
    level = instance.level if getattr(instance, "level", None) else "L2"
    return f"study_material/{subject_name}/{level}/{filename}"


class StudyMaterial(models.Model):
    LEVEL_CHOICES = [
        ("L2", "Level 2"),
        ("L3", "Level 3"),
        ("L4", "Level 4"),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="study_materials")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default="L2")
    material_file = models.FileField(upload_to=study_material_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.level})"
