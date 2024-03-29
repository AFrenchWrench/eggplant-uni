from django.db import models
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='courses')
    prerequisites = models.ManyToManyField('Course', related_name='prerequisite_for', blank=True)
    corequisites = models.ManyToManyField('Course', related_name='corequisite_for', blank=True)
    units = models.PositiveIntegerField()
    type = models.CharField(max_length=20,
                            choices=[('G', 'General'), ('M', 'Major'), ('F', 'Foundation'), ('E', 'Elective')])


class SemesterCourse(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='semester_courses')
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='semester_courses')
    day_and_time = models.CharField(max_length=100)
    exam_datetime = models.DateTimeField()
    exam_location = models.CharField(max_length=100)
    professor = models.ForeignKey('users.Professor', on_delete=models.CASCADE, related_name='semester_courses')
    capacity = models.PositiveIntegerField()


class StudentCourse(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='courses', null=True)
    course = models.ForeignKey('SemesterCourse', on_delete=models.CASCADE, related_name='student_courses',
                               null=True)
    grade = models.FloatField()

    def is_passed(self):
        if self.grade >= 10:
            return True
        else:
            return False

    def course_status(self):
        return 'In Progress' if self.course.semester.is_active() else 'Passed'


class Semester(models.Model):
    name = models.CharField(max_length=100)
    course_selection_start_time = models.DateTimeField()
    course_selection_end_time = models.DateTimeField()
    class_start_time = models.DateTimeField()
    class_end_time = models.DateTimeField()
    course_addition_drop_start = models.DateTimeField()
    course_addition_drop_end = models.DateTimeField()
    last_day_for_emergency_withdrawal = models.DateTimeField()
    exam_start_time = models.DateTimeField()
    semester_end_date = models.DateField()

    def is_active(self):
        return True if self.semester_end_date >= timezone.now() else False


class SemesterStudent(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='semester_students')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE, related_name='semester_students')
    is_active = models.BooleanField(default=True)


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Major(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='majors')
    units = models.PositiveIntegerField()
    degree_level = models.CharField(max_length=20, choices=(
        ('AD', "Associate's Degree"), ('BD', "Bachelor's Degree"), ('MD', "Master's Degree"),
        ('D', "Doctorate or Ph.D."),
        ('PD', "Professional Degrees")))
