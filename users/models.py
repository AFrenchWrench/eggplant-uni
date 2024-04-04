from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    national_id = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    user_code = models.CharField(max_length=255, unique=True)


class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='student')
    admission_year = models.PositiveIntegerField()
    admission_semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='students')
    major = models.ForeignKey('university.Major', on_delete=models.CASCADE, related_name='students')
    advisor = models.ForeignKey('Professor', on_delete=models.CASCADE, null=True, blank=True)
    military_status = models.BooleanField(default=False)

    def get_gpa(self):
        return self.courses.aggregate(average_grade=Avg('grade'))['average_grade']

    def get_military_status(self):
        if self.user.gender == 'M':
            return self.military_status
        else:
            return True

    def get_academic_semester_count(self):
        return self.semester_students.filter(is_active=True).count()


class Professor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='professor')
    major = models.ForeignKey('university.Major', on_delete=models.CASCADE, related_name='professors')
    specialization = models.CharField(max_length=50)
    rank = models.CharField(max_length=2, choices=(
        ('I', 'Instructor'), ('A1', 'Assistant Professor'), ('A2', 'Associate Professor'), ('P', 'Professor')))


class Assistant(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='assistant')
    faculty = models.ForeignKey('university.Faculty', on_delete=models.CASCADE, related_name='assistants')
    major = models.ForeignKey('university.Major', on_delete=models.CASCADE, related_name='assistants')
