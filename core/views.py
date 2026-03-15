import os
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import RegisterForm
from .models import (
    PaperProgress,
    PastPaper,
    StudentProfile,
    Subject,
    Video,
    VideoProgress,
)

VALID_LEVELS = ["L2", "L3", "L4"]


def _build_subject_cards(selected_level=""):
    subjects = Subject.objects.all().order_by("name")
    subject_cards = []

    for subject in subjects:
        level_summary = []
        has_selected_level = False
        total_resources = 0

        for level in VALID_LEVELS:
            video_count = Video.objects.filter(subject=subject, level=level).count()
            paper_count = PastPaper.objects.filter(subject=subject, level=level).count()
            has_content = video_count > 0 or paper_count > 0

            if has_content:
                total_resources += video_count + paper_count
                level_summary.append(
                    {
                        "code": level,
                        "video_count": video_count,
                        "paper_count": paper_count,
                        "has_content": has_content,
                    }
                )

            if selected_level == level and has_content:
                has_selected_level = True

        if selected_level and not has_selected_level:
            continue

        subject_cards.append(
            {
                "subject": subject,
                "levels": level_summary,
                "total_resources": total_resources,
            }
        )

    return subject_cards


def home(request):
    selected_level = request.GET.get("level", "").strip()
    if selected_level not in VALID_LEVELS:
        selected_level = ""

    subject_cards = _build_subject_cards(selected_level)

    return render(
        request,
        "core/index.html",
        {
            "subject_cards": subject_cards,
            "selected_level": selected_level,
            "valid_levels": VALID_LEVELS,
        },
    )


@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    selected_level = request.GET.get("level", "").strip()
    if selected_level not in VALID_LEVELS:
        selected_level = ""

    level_cards = []
    for level in VALID_LEVELS:
        video_count = Video.objects.filter(subject=subject, level=level).count()
        paper_count = PastPaper.objects.filter(subject=subject, level=level).count()
        if video_count > 0 or paper_count > 0:
            level_cards.append(
                {
                    "code": level,
                    "video_count": video_count,
                    "paper_count": paper_count,
                    "is_selected": selected_level == level,
                }
            )

    return render(
        request,
        "core/subject_detail.html",
        {
            "subject": subject,
            "level_cards": level_cards,
            "selected_level": selected_level,
            "valid_levels": VALID_LEVELS,
        },
    )


@login_required
def videos_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    level = request.GET.get("level", "").strip()

    if level in VALID_LEVELS:
        videos = Video.objects.filter(subject=subject, level=level).order_by("title", "-uploaded_at")
    else:
        videos = Video.objects.none()
        level = ""

    completed_video_ids = set(
        VideoProgress.objects.filter(student=request.user, completed=True)
        .values_list("video_id", flat=True)
    )

    return render(
        request,
        "core/videos_by_subject.html",
        {
            "subject": subject,
            "videos": videos,
            "selected_level": level,
            "valid_levels": VALID_LEVELS,
            "completed_video_ids": completed_video_ids,
        },
    )


@login_required
def past_papers_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    level = request.GET.get("level", "").strip()

    if level in VALID_LEVELS:
        papers = PastPaper.objects.filter(subject=subject, level=level).order_by("title", "-uploaded_at")
    else:
        papers = PastPaper.objects.none()
        level = ""

    viewed_paper_ids = set(
        PaperProgress.objects.filter(student=request.user, viewed=True)
        .values_list("paper_id", flat=True)
    )

    return render(
        request,
        "core/past_papers_by_subject.html",
        {
            "subject": subject,
            "papers": papers,
            "selected_level": level,
            "valid_levels": VALID_LEVELS,
            "viewed_paper_ids": viewed_paper_ids,
        },
    )


def about(request):
    return render(request, "core/about.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def contact(request):
    return render(request, "core/contact.html")


def terms(request):
    return render(request, "core/terms.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})


@login_required
def dashboard(request):
    total_videos = Video.objects.count()
    completed_videos = VideoProgress.objects.filter(
        student=request.user,
        completed=True
    ).count()

    total_papers = PastPaper.objects.count()
    viewed_papers = PaperProgress.objects.filter(
        student=request.user,
        viewed=True
    ).count()

    overall_video_percent = 0
    if total_videos > 0:
        overall_video_percent = int((completed_videos / total_videos) * 100)

    subject_stats = Subject.objects.annotate(
        total_subject_videos=Count("videos", distinct=True),
        total_subject_papers=Count("past_papers", distinct=True),
        completed_subject_videos=Count(
            "videos__progress_records",
            filter=Q(
                videos__progress_records__student=request.user,
                videos__progress_records__completed=True,
            ),
            distinct=True,
        ),
        viewed_subject_papers=Count(
            "past_papers__progress_records",
            filter=Q(
                past_papers__progress_records__student=request.user,
                past_papers__progress_records__viewed=True,
            ),
            distinct=True,
        ),
    )

    enriched_subject_stats = []
    for subject in subject_stats:
        percent = 0
        if subject.total_subject_videos > 0:
            percent = int((subject.completed_subject_videos / subject.total_subject_videos) * 100)

        enriched_subject_stats.append(
            {
                "subject": subject,
                "total_videos": subject.total_subject_videos,
                "completed_videos": subject.completed_subject_videos,
                "total_papers": subject.total_subject_papers,
                "viewed_papers": subject.viewed_subject_papers,
                "percent": percent,
            }
        )

    recent_video_progress = VideoProgress.objects.filter(student=request.user).select_related(
        "video", "video__subject"
    )[:5]

    recent_paper_progress = PaperProgress.objects.filter(student=request.user).select_related(
        "paper", "paper__subject"
    )[:5]

    return render(
        request,
        "core/dashboard.html",
        {
            "total_videos": total_videos,
            "completed_videos": completed_videos,
            "total_papers": total_papers,
            "viewed_papers": viewed_papers,
            "overall_video_percent": overall_video_percent,
            "subject_stats": enriched_subject_stats,
            "recent_video_progress": recent_video_progress,
            "recent_paper_progress": recent_paper_progress,
        },
    )


@login_required
def mark_video_complete(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    VideoProgress.objects.update_or_create(
        student=request.user,
        video=video,
        defaults={"completed": True},
    )

    return redirect(f"{reverse('videos_by_subject', kwargs={'subject_id': video.subject.id})}?level={video.level}")


@login_required
def mark_paper_viewed(request, paper_id):
    paper = get_object_or_404(PastPaper, id=paper_id)

    PaperProgress.objects.update_or_create(
        student=request.user,
        paper=paper,
        defaults={"viewed": True},
    )

    return redirect(f"{reverse('past_papers_by_subject', kwargs={'subject_id': paper.subject.id})}?level={paper.level}")


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

    return HttpResponse("Superuser already exists.")
