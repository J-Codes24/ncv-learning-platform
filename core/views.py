from django.shortcuts import render, get_object_or_404
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