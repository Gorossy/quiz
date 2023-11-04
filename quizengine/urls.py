from django.urls import path
from .views import ExamListView, ExamDetailView, SubmitExamView, UserStatisticsView

urlpatterns = [
    path('exams/', ExamListView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('submit-exam/', SubmitExamView.as_view(), name='submit-exam'),
    path('user-statistics/', UserStatisticsView.as_view(), name='user-statistics'),
]