from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


class User(AbstractUser):
    email = models.EmailField(unique=True, help_text='Required. Inform a valid email address.')
    phone_number = models.CharField(max_length=11, unique=True, help_text='Required (09) 9-digit phone')
    national_id = models.CharField(max_length=10, unique=True, help_text='10 digit national id')
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')],
                              help_text='M for Male/F for Female')
    birth_date = models.DateField(null=True, blank=True,
                                  help_text='Date of birth in date format : YYYY-MM-DD or YYYY/MM/DD')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    user_code = models.CharField(max_length=255, unique=True,
                                 help_text='Unique user code that varies based on user type')


class Student(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='student',
                                help_text='User To Student Relation')
    admission_year = models.PositiveIntegerField(help_text='Admission Year in Integer format 2023 2024 ...')
    admission_semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='students',
                                           help_text='Student To Semester Relation')
    major = models.ForeignKey('university.Major', on_delete=models.CASCADE, related_name='students',
                              help_text='Student To Major Relation')
    advisor = models.ForeignKey('Professor', on_delete=models.CASCADE, null=True, blank=True, related_name='students',
                                help_text='Student To Advisor Relation')
    military_status = models.BooleanField(default=False, help_text='Mandatory Military Status')

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
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='professor',
                                help_text='Professor To User Relation')
    major = models.ForeignKey('university.Major', on_delete=models.CASCADE, related_name='professors',
                              help_text='Professor To Major Relation')
    specialization = models.CharField(max_length=50, help_text='Professor\'s Specialization')
    rank = models.CharField(max_length=2, choices=(
        ('I', 'Instructor'), ('A1', 'Assistant Professor'), ('A2', 'Associate Professor'), ('P', 'Professor')),
                            help_text="Professor's Rank ('I', 'Instructor'),"
                                      "('A1', 'Assistant Professor'), "
                                      "('A2', 'Associate Professor'), ('P', 'Professor')")


class Assistant(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='assistant',
                                help_text="Assistant To User Relation")
    faculty = models.ForeignKey('university.Faculty', on_delete=models.CASCADE, related_name='assistants',
                                help_text="Assistant To Faculty Relation")
    major = models.ForeignKey('university.Major', on_delete=models.CASCADE, related_name='assistants',
                              help_text="Assistant To Major Relation")
