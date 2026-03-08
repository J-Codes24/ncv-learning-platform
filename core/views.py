import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import Subject, Video, PastPaper


def home(request):
    subjects = Subject.objects.all()
    return render(request, 'core/index.html', {'subjects': subjects})


def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'core/subject_detail.html', {'subject': subject})


def videos_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    videos = Video.objects.filter(subject=subject)

    level = request.GET.get('level')
    if level:
        videos = videos.filter(level=level)

    return render(request, 'core/videos_by_subject.html', {
        'subject': subject,
        'videos': videos,
    })


def past_papers_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    papers = PastPaper.objects.filter(subject=subject)

    level = request.GET.get('level')
    if level:
        papers = papers.filter(level=level)

    return render(request, 'core/past_papers_by_subject.html', {
        'subject': subject,
        'papers': papers,
    })


def create_admin(request):
    User = get_user_model()

    username = os.getenv("ADMIN_USERNAME")
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not username or not email or not password:
        return HttpResponse("Admin environment variables are missing.")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        return HttpResponse("Superuser created successfully.")
    else:
        return HttpResponse("Superuser already exists.")