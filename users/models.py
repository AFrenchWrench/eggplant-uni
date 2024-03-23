from django.contrib.auth.models import AbstractUser
from django.db import models

from users.utils import generate_student_id, generate_assistant_id, generate_professor_id


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    national_id = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)


class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='student')
    code = models.CharField(default=generate_student_id, max_length=8, editable=False, unique=True)
    year_of_admission = models.PositiveIntegerField()
    admission_semester = models.CharField(max_length=20)
    grade = models.FloatField()
    faculty = models.ForeignKey('university.Faculty', on_delete=models.PROTECT)
    major = models.ForeignKey('university.Major', on_delete=models.PROTECT)
    completed_courses = models.ManyToManyField('university.ApprovedCourse', related_name='completed_by',
                                               blank=True)
    courses_in_progress = models.ManyToManyField('university.ApprovedCourse', related_name='in_progress_by',
                                                 blank=True)
    advisor = models.ForeignKey('Professor', on_delete=models.SET_NULL, null=True, blank=True)
    military_status = models.BooleanField(default=False)
    remaining_semesters = models.IntegerField()


class Professor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='professor')
    code = models.CharField(default=generate_professor_id, max_length=8, editable=False, unique=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.PROTECT)
    major = models.ForeignKey('university.Major', on_delete=models.PROTECT)
    specialization = models.CharField(max_length=100)
    rank = models.CharField(max_length=50)
    past_taught_courses = models.ManyToManyField('university.ApprovedCourse',
                                                 related_name='past_taught_courses', blank=True)


class Assistant(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='assistant')
    code = models.CharField(default=generate_assistant_id, max_length=8, editable=False, unique=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.PROTECT)
    major = models.ForeignKey('university.Major', on_delete=models.PROTECT)
