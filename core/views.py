import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import Subject, Video, PastPaper

VALID_LEVELS = ['L2', 'L3', 'L4']


def home(request):
    subjects = Subject.objects.all()
    return render(request, 'core/index.html', {'subjects': subjects})


def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'core/subject_detail.html', {'subject': subject})


def videos_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    level = request.GET.get('level', '').strip()

    if level in VALID_LEVELS:
        videos = Video.objects.filter(subject=subject, level=level)
    else:
        videos = Video.objects.none()
        level = ''

    return render(request, 'core/videos_by_subject.html', {
        'subject': subject,
        'videos': videos,
        'selected_level': level,
        'valid_levels': VALID_LEVELS,
    })


def past_papers_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    level = request.GET.get('level', '').strip()

    if level in VALID_LEVELS:
        papers = PastPaper.objects.filter(subject=subject, level=level)
    else:
        papers = PastPaper.objects.none()
        level = ''

    return render(request, 'core/past_papers_by_subject.html', {
        'subject': subject,
        'papers': papers,
        'selected_level': level,
        'valid_levels': VALID_LEVELS,
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
