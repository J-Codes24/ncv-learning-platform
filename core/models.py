from django.db import models
import os


def paper_upload_path(instance, filename):
    return os.path.join('past_papers', filename)


def video_upload_path(instance, filename):
    return os.path.join('videos', filename)


class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='subjects/', blank=True, null=True)

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
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    video_file = models.FileField(upload_to=video_upload_path)
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
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    paper_file = models.FileField(upload_to=paper_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.title} ({self.level})"