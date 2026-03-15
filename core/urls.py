from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('contact/', views.contact, name='contact'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:subject_id>/videos/', views.videos_by_subject, name='videos_by_subject'),
    path('subject/<int:subject_id>/papers/', views.past_papers_by_subject, name='past_papers_by_subject'),
    path('video/<int:video_id>/complete/', views.mark_video_complete, name='video_complete'),
    path('paper/<int:paper_id>/viewed/', views.mark_paper_viewed, name='paper_viewed'),
    path('create-admin/', views.create_admin, name='create_admin'),
]