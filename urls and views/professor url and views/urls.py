from django.urls import path
from .views import (
    ProfessorListView,
    ProfessorDetailView,
    ProfessorCourseAppealRequestsListView,
    ProfessorCourseAppealRequestDetailView,
    ProfessorCourseApproveView,
    ProfessorCourseScoresCreateView,
    ProfessorStudentsSelectionFormsView,
    ProfessorStudentsSelectionFormDetailView,
    ProfessorStudentsSubstitutionFormsView,
    ProfessorStudentsSubstitutionFormDetailView, ProfessorStudentsSubstitutionFormSubmitView, ProfessorCourseScoresView,
)

urlpatterns = [
    # Professors
    path('', ProfessorListView.as_view(), name='professor-list'),
    path('<int:pk>/', ProfessorDetailView.as_view(), name='professor-detail'),

    # Professor Students Selection Forms
    path('<int:pk>/students-selection-forms/', ProfessorStudentsSelectionFormsView.as_view(),
         name='professor-students-selection-forms'),
    path('<int:pk>/students-selection-forms/<int:s_pk>/', ProfessorStudentsSelectionFormDetailView.as_view(),
         name='professor-students-selection-form-detail'),

    # Professor Students Substitution Forms
    path('students-substitution-forms/', ProfessorStudentsSubstitutionFormsView.as_view(),
         name='professor-students-substitution-forms'),
    path('students-substitution-forms/<int:pk>/', ProfessorStudentsSubstitutionFormDetailView.as_view(),
         name='professor-students-substitution-form-detail'),

    # Professor Course Appeal Requests
    path('<int:pk>/courses/<int:s_pk>/appeal-requests/', ProfessorCourseAppealRequestsListView.as_view(),
         name='professor-course-appeal-requests'),
    path('<int:pk>/courses/<int:c_pk>/appeal-requests/<int:r_pk>/',
         ProfessorCourseAppealRequestDetailView.as_view(), name='professor-course-appeal-request-detail'),
    path('<int:pk>/courses/<int:c_pk>/appeal-requests/<int:r_pk>/',
         ProfessorCourseAppealRequestDetailView.as_view(), name='professor-course-appeal-request-create'),

    # Professor Course Approve
    path('<int:pk>/courses/<int:c_pk>/approve/', ProfessorCourseApproveView.as_view(),
         name='professor-course-approve'),

    # Professor Course Scores
    path('<int:pk>/courses/<int:c_pk>/scores/', ProfessorCourseScoresCreateView.as_view(),
         name='professor-course-scores'),

    # Professor Students Selection Forms
    path('<int:pk>/students-selection-forms/', ProfessorStudentsSelectionFormsView.as_view(),
         name='professor-students-selection-forms'),
    path('<int:pk>/students-selection-forms/<int:s_pk>/', ProfessorStudentsSelectionFormDetailView.as_view(),
         name='professor-students-selection-form-detail'),

    # Professor Students Substitution Forms
    path('<int:pk>/students-substitution-forms/', ProfessorStudentsSubstitutionFormsView.as_view(),
         name='professor-students-substitution-forms'),
    path('<int:pk>/students-substitution-forms/<int:s_pk>/',
         ProfessorStudentsSubstitutionFormDetailView.as_view(), name='professor-students-substitution-form-detail'),

    path('<int:pk>/students-substitution-forms/<int:s_pk>/',
         ProfessorStudentsSubstitutionFormSubmitView.as_view(), name='professor-students-substitution-form-submit'),

    # Professor Course Scores
    path('<int:pk>/courses/<int:c_pk>/scores/', ProfessorCourseScoresView.as_view(),
         name='professor-course-scores'),
]
