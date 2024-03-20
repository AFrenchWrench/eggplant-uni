from django.urls import path
from .views import (
    SemesterListView,
    SemesterDetailView,
    ApprovedCourseDetailView,
    ApprovedCourseListView,
    SemesterCourseListView,
    SemesterCourseDetailView,
)

urlpatterns = [
    # Subjects
    path('approved_courses/', ApprovedCourseListView.as_view(), name='subject-list'),
    path('approved_course/<int:pk>/', ApprovedCourseDetailView.as_view(), name='subject-detail'),

    # Courses
    path('semester_courses/', SemesterCourseListView.as_view(), name='course-list'),
    path('semester_course/<int:pk>/', SemesterCourseDetailView.as_view(), name='course-detail'),

    # Semesters
    path('semesters/', SemesterListView.as_view(), name='semester-list'),
    path('semester/<int:pk>/', SemesterDetailView.as_view(), name='semester-detail'),

]