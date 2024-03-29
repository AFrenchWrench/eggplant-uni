from django.contrib import admin
from .models import (
    Course,
    SemesterCourse,
    StudentCourse,
    Semester,
    SemesterStudent,
    Faculty,
    Major,
)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty', 'units', 'type']


@admin.register(SemesterCourse)
class SemesterCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'semester', 'day_and_time', 'exam_datetime', 'exam_location', 'professor', 'capacity']


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'is_passed', 'course_status']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_selection_start_time', 'course_selection_end_time', 'class_start_time',
                    'class_end_time', 'course_addition_drop_start', 'course_addition_drop_end',
                    'last_day_for_emergency_withdrawal', 'exam_start_time', 'semester_end_date', 'is_active']


@admin.register(SemesterStudent)
class SemesterStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'is_active']


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'faculty', 'units', 'degree_level']
