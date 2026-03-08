from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('subject/<int:subject_id>/videos/', views.videos_by_subject, name='videos_by_subject'),
    path('subject/<int:subject_id>/papers/', views.past_papers_by_subject, name='past_papers_by_subject'),
    path('create-admin/', views.create_admin, name='create_admin'),
]