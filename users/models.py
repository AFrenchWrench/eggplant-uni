import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=8, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    national_id = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    type = models.CharField(max_length=10,
                            choices=[('S', 'student'), ('I', 'it manager'), ('P', 'professor'), ('A', 'assistant')])


class Student(models.Model):
    student_id = models.OneToOneField('User', on_delete=models.CASCADE)
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
    professor_id = models.OneToOneField('User', on_delete=models.CASCADE)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.PROTECT)
    major = models.ForeignKey('university.Major', on_delete=models.PROTECT)
    specialization = models.CharField(max_length=100)
    rank = models.CharField(max_length=50)
    past_taught_courses = models.ManyToManyField('university.ApprovedCourse',
                                                 related_name='past_taught_courses', blank=True)


class Assistant(models.Model):
    assistant_id = models.OneToOneField('User', on_delete=models.CASCADE)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.PROTECT)
    major = models.ForeignKey('university.Major', on_delete=models.PROTECT)
