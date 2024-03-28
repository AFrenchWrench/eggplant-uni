from django.urls import path

from .views import (
    StudentListView,
    StudentDetailView,
    StudentMyCoursesView,
    PassCoursesReportView,
    StudentSemesterCoursesView,
    StudentRemainingSemestersView,
    StudentCourseSelectionCreateView,
    StudentCourseSelectionView,
    StudentCourseSelectionSendFormView,
    CourseSelectionCheckView,
    CourseSelectionSubmitView,
    CourseSubstitutionCreateView,
    CourseSubstitutionListView,
    CourseSubstitutionCheckView,
    CourseSubstitutionSubmitView,
    CourseSubstitutionSendFormView, ClassScheduleView, ExamScheduleView, EmergencyRemoveCourseView, RemoveSemesterView,
    StudentCourseAppealRequestView, StudentStudyingEvidenceView,
)

urlpatterns = [
    # Students
    path('', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Student My Courses
    path('<int:pk>/my-courses/', StudentMyCoursesView.as_view(), name='student-my-courses'),

    path('<int:pk>/pass-courses-report/', PassCoursesReportView.as_view(), name='pass-courses-report'),

    # Student Term Courses
    path('<int:pk>/semester-courses/', StudentSemesterCoursesView.as_view(), name='student-term-courses'),

    # Student Remaining Semesters
    path('<int:pk>/remaining-semesters/', StudentRemainingSemestersView.as_view(),
         name='student-remaining-semesters'),

    # Student Course Selection
    path('<int:pk>/course-selection/create/', StudentCourseSelectionCreateView.as_view(),
         name='student-course-selection-create'),
    path('<int:pk>/course-selection/', StudentCourseSelectionView.as_view(), name='student-course-selection'),

    # Course Selection Check
    path('<int:pk>/course-selection/check/', CourseSelectionCheckView.as_view(), name='course-selection-check'),

    # Course Selection Submit
    path('<int:pk>/course-selection/submit/', CourseSelectionSubmitView.as_view(),
         name='course-selection-submit'),

    path('<int:pk>/course-selection/send-form/', StudentCourseSelectionSendFormView.as_view(),
         name='student-course-selection-send-form'),

    # Course Substitution Create
    path('<int:pk>/course-substitution/create/', CourseSubstitutionCreateView.as_view(),
         name='course-substitution-create'),

    # Course Substitution List
    path('<int:pk>/course-substitution/', CourseSubstitutionListView.as_view(),
         name='course-substitution-list'),

    # Course Substitution Check
    path('<int:pk>/course-substitution/check/', CourseSubstitutionCheckView.as_view(),
         name='course-substitution-check'),

    # Course Substitution Submit
    path('<int:pk>/course-substitution/submit/', CourseSubstitutionSubmitView.as_view(),
         name='course-substitution-submit'),

    # Course Substitution Send Form
    path('<int:pk>/course-substitution/send-form/', CourseSubstitutionSendFormView.as_view(),
         name='course-substitution-send-form'),

    # Class Schedule
    path('<int:pk>/class-schedule/', ClassScheduleView.as_view(), name='class-schedule'),

    # Exam Schedule
    path('<int:pk>/exam-schedule/', ExamScheduleView.as_view(), name='exam-schedule'),

    # Emergency Remove Course
    path('<int:pk>/courses/<int:c_pk>/emergency-remove/', EmergencyRemoveCourseView.as_view(),
         name='emergency-remove-course'),

    # Remove Term
    path('<int:pk>/remove-semester/', RemoveSemesterView.as_view(), name='remove-semester'),

    # Student Course Appeal Request
    path('<int:pk>/courses/<int:c_pk>/appeal-request/', StudentCourseAppealRequestView.as_view(),
         name='student-course-appeal-request'),

    # Student Studying Evidence
    path('student/<int:pk>/studying-evidence/', StudentStudyingEvidenceView.as_view(),
         name='student-studying-evidence'),

]
