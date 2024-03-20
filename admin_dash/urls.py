from django.urls import path
from .views import (
    ProfessorListView,
    ProfessorDetailView,
    StudentListView,
    StudentDetailView,
    AssistantListView,
    AssistantDetailView,
    FacultyListView,
    FacultyDetailView,
    SemesterListView,
    SemesterDetailView,
)

urlpatterns = [
    # Professors
    path('professors/', ProfessorListView.as_view(), name='professor-list'),
    path('professor/<int:pk>/', ProfessorDetailView.as_view(), name='professor-detail'),

    # Students
    path('students/', StudentListView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Assistants
    path('assistants/', AssistantListView.as_view(), name='assistant-list'),
    path('assistant/<int:pk>/', AssistantDetailView.as_view(), name='assistant-detail'),

    # Faculties
    path('faculties/', FacultyListView.as_view(), name='faculty-list'),
    path('faculty/<int:pk>/', FacultyDetailView.as_view(), name='faculty-detail'),

    # Semesters
    path('semesters/', SemesterListView.as_view(), name='semester-list'),
    path('semester/<int:pk>/', SemesterDetailView.as_view(), name='semester-detail'),

]
