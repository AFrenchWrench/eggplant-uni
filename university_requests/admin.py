from django.contrib import admin
from .models import (
    CourseRegistrationRequest,
    StudentCourseParticipant,
    CourseCorrectionRequest,
    ReconsiderationRequest,
    EmergencyWithdrawalRequest,
    SemesterWithdrawalRequest,
    DefermentRequest,
)


@admin.register(CourseRegistrationRequest)
class CourseRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'status']


@admin.register(StudentCourseParticipant)
class StudentCourseParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'status']


@admin.register(CourseCorrectionRequest)
class CourseCorrectionRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'status']


@admin.register(ReconsiderationRequest)
class ReconsiderationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'status']


@admin.register(EmergencyWithdrawalRequest)
class EmergencyWithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course', 'status']


@admin.register(SemesterWithdrawalRequest)
class SemesterWithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'semester', 'status']


@admin.register(DefermentRequest)
class DefermentRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'semester', 'faculty']
