from django.db import models

from users.utils import generate_4_length_code


class ApprovedCourse(models.Model):
    course_code = models.CharField(default=generate_4_length_code, max_length=4, editable=False, unique=True)
    course_name = models.CharField(max_length=100)
    offering_faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT)
    prerequisites = models.ManyToManyField('ApprovedCourse', related_name='prerequisite_for', blank=True)
    corequisites = models.ManyToManyField('ApprovedCourse', related_name='corequisite_for', blank=True)
    number_of_credits = models.PositiveIntegerField()
    course_type = models.CharField(max_length=20,
                                   choices=[('General', 'General'), ('Major', 'Major'), ('Foundation', 'Foundation'),
                                            ('Elective', 'Elective')])

    def save(self, *args, **kwargs):
        if not self.course_code:
            self.course_code = generate_4_length_code()
        super(ApprovedCourse, self).save(*args, **kwargs)


class SemesterCourse(models.Model):
    course = models.ForeignKey('ApprovedCourse', on_delete=models.PROTECT)
    academic_semester = models.ForeignKey('Semester', on_delete=models.PROTECT)
    day_and_time = models.CharField(max_length=100)
    exam_date_and_time = models.DateTimeField()
    exam_location = models.CharField(max_length=100)
    professor = models.ForeignKey('users.Professor', on_delete=models.PROTECT)
    course_capacity = models.PositiveIntegerField()


class Semester(models.Model):
    semester_code = models.CharField(default=generate_4_length_code, max_length=4, editable=False, unique=True)
    semester_name = models.CharField(max_length=100)
    registered_students_and_professors = models.ManyToManyField('users.User', related_name='semesters', blank=True)
    semester_courses = models.ManyToManyField('ApprovedCourse', related_name='course_semester', blank=True)
    course_selection_start_time = models.DateTimeField()
    course_selection_end_time = models.DateTimeField()
    class_start_time = models.DateTimeField()
    class_end_time = models.DateTimeField()
    course_addition_drop_start = models.DateTimeField()
    course_addition_drop_end = models.DateTimeField()
    last_day_for_emergency_withdrawal = models.DateTimeField()
    exam_start_time = models.DateTimeField()
    semester_end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.semester_code:
            self.semester_code = generate_4_length_code()
        super(Semester, self).save(*args, **kwargs)


class Faculty(models.Model):
    faculty_code = models.CharField(default=generate_4_length_code, max_length=4, editable=False, unique=True)
    faculty_name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.faculty_code:
            self.faculty_code = generate_4_length_code()
        super(Faculty, self).save(*args, **kwargs)


class Major(models.Model):
    major_code = models.CharField(default=generate_4_length_code, max_length=4, editable=False, unique=True)
    major_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', on_delete=models.PROTECT)
    number_of_credits = models.PositiveIntegerField()
    degree_level = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.major_code:
            self.major_code = generate_4_length_code()
        super(Major, self).save(*args, **kwargs)
