from django.db import models


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
        ('L2', 'Level 2'),
        ('L3', 'Level 3'),
        ('L4', 'Level 4'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='L2')
    video_file = models.FileField(upload_to=video_upload_path, blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.level})"


class PastPaper(models.Model):
    LEVEL_CHOICES = [
        ('L2', 'Level 2'),
        ('L3', 'Level 3'),
        ('L4', 'Level 4'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='past_papers')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='L2')
    paper_file = models.FileField(upload_to=paper_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.level})"