from django.contrib import admin
from .models import (
    User,
    Student,
    Professor,
    Assistant,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'gender', 'birth_date', 'user_code']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'admission_year', 'admission_semester', 'major', 'advisor', 'military_status']


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['user', 'major', 'specialization', 'rank']


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ['user', 'faculty', 'major']
