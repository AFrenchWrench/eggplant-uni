from django.urls import path
from .views import (
    AssistantCourseProfApprovedListView,
    AssistantCourseProfApprovedDetailView,
    AssistantStudyingEvidenceListView,
    AssistantStudyingEvidenceDetailView,
    AssistantRemoveTermListView,
    AssistantRemoveTermDetailView,
    AssistantEmergencyRemoveListView,
    AssistantEmergencyRemoveDetailView,
)

urlpatterns = [

    # Assistant Course Prof Approved List
    path('<int:pk>/courses/<int:c_pk>/prof-approved/', AssistantCourseProfApprovedListView.as_view(),
         name='assistant-course-prof-approved-list'),

    # Assistant Course Prof Approved Detail
    path('<int:pk>/courses/<int:c_pk>/prof-approved/<int:s_pk>/',
         AssistantCourseProfApprovedDetailView.as_view(), name='assistant-course-prof-approved-detail'),

    # Assistant Studying Evidence List
    path('<int:pk>/studying-evidence/', AssistantStudyingEvidenceListView.as_view(),
         name='assistant-studying-evidence-list'),

    # Assistant Studying Evidence Detail
    path('<int:pk>/studying-evidence/<int:s_pk>/', AssistantStudyingEvidenceDetailView.as_view(),
         name='assistant-studying-evidence-detail'),

    # Assistant Remove Term List
    path('<int:pk>/remove-term/', AssistantRemoveTermListView.as_view(), name='assistant-remove-term-list'),

    # Assistant Remove Term Detail
    path('<int:pk>/remove-term/<int:s_pk>/', AssistantRemoveTermDetailView.as_view(),
         name='assistant-remove-term-detail'),

    # Assistant Emergency Remove List
    path('<int:pk>/emergency-remove/', AssistantEmergencyRemoveListView.as_view(),
         name='assistant-emergency-remove-list'),

    # Assistant Emergency Remove Detail
    path('<int:pk>/emergency-remove/<int:s_pk>/', AssistantEmergencyRemoveDetailView.as_view(),
         name='assistant-emergency-remove-detail'),
]
