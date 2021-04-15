from django.urls import path
from .views import DayListView, UpdateFormView, ParticipantView, ATLeaderboardView

urlpatterns = [
    path('tracker/updateform/', UpdateFormView.as_view(), name='updateform'),
    path('', DayListView.as_view(),name='home'),
    path('tracker/<int:pk>/', ParticipantView.as_view(), name='dailyparticipants'),
    path('tracker/leaderboard/', ATLeaderboardView.as_view(), name= 'leaderboard'),
]