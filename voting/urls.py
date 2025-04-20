from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('total_votes/', views.total_votes, name='total_votes'),
    path('edit_candidates/', views.edit_candidates, name='edit_candidates'),
    path('reset_vote/', views.reset_vote, name='reset_vote'),
    path('cast_vote/', views.cast_vote, name='cast_vote'),
    path('vote_candidate/', views.vote_candidate, name='vote_candidate'),
]