from datetime import date

from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Course name in Eng")
    major = models.ForeignKey('Major', on_delete=models.CASCADE, related_name='courses',
                              help_text="Course To Major Relation")
    prerequisites = models.ManyToManyField('Course', related_name='prerequisite_for', blank=True,
                                           help_text="Prerequisites for a course relation")
    corequisites = models.ManyToManyField('Course', related_name='corequisite_for', blank=True,
                                          help_text="Corequisites for a course relation")
    units = models.PositiveIntegerField(help_text="Number of units")
    type = models.CharField(max_length=20,
                            choices=[('G', 'General'), ('M', 'Major'), ('F', 'Foundation'), ('E', 'Elective')],
                            help_text="Course Type ('G', 'General'), ('M', 'Major'), "
                                      "('F', 'Foundation'), ('E', 'Elective')")

    def get_all_prerequisites(self):
        prerequisites = list(self.prerequisites.all())
        for prerequisite in self.prerequisites.all():
            prerequisites.extend(prerequisite.get_all_prerequisites())
        return prerequisites


class SemesterCourse(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='semester_courses',
                               help_text="Semester course To course Relation")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='semester_courses',
                                 help_text="Semester course to semester Relation")
    day_and_time = models.CharField(max_length=100, help_text="Course Day and Time period")
    exam_datetime = models.DateTimeField(help_text="Course Exam Time")
    exam_location = models.CharField(max_length=100, help_text="Course Exam Location")
    professor = models.ForeignKey('users.Professor', on_delete=models.CASCADE, related_name='semester_courses',
                                  help_text="Semester Course To professor Relation")
    capacity = models.PositiveIntegerField(help_text="Course Capacity")

    def get_capacity_count(self):
        return self.capacity - self.student_courses.count()

    def course_units(self):
        return self.course.units


class StudentCourse(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='courses', null=True,
                                help_text="Student Course To Student Relation")
    course = models.ForeignKey('SemesterCourse', on_delete=models.CASCADE, related_name='student_courses',
                               null=True, help_text="Student Course To Student Relation")
    grade = models.FloatField(help_text="Course Grade", default=0)

    def is_passed(self):
        if self.grade >= 10.00:
            return True
        else:
            return False

    def course_status(self):
        return 'In Progress' if self.course.semester.is_active() else 'Passed'


class Semester(models.Model):
    name = models.CharField(max_length=100, help_text="Semester Name")
    course_selection_start_time = models.DateTimeField(help_text="Semester Selection Start Time")
    course_selection_end_time = models.DateTimeField(help_text="Semester Selection End Time")
    class_start_time = models.DateTimeField(help_text="Class Start Time")
    class_end_time = models.DateTimeField(help_text="Class End Time")
    course_addition_drop_start = models.DateTimeField(help_text="Semester Addition Drop Start Time")
    course_addition_drop_end = models.DateTimeField(help_text="Semester Addition Drop End Time")
    last_day_for_emergency_withdrawal = models.DateTimeField(help_text="Last Day For Emergency Withdrawal")
    exam_start_time = models.DateTimeField(help_text="Exam Start Time")
    semester_end_date = models.DateField(help_text="Semester End Time")

    def is_active(self):
        if self.semester_end_date >= date.today():
            self.is_active = True
            return True
        else:
            self.is_active = False
            return False


class SemesterStudent(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='semester_students',
                                help_text="Semester Student To Student Relation")
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE, related_name='semester_students',
                                 help_text="Semester Student to Semester Relation")
    is_active = models.BooleanField(default=True, help_text="Whether a Student is Active")


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Faculty Name")


class Major(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Major Name")
    department = models.CharField(max_length=100, help_text="Major Department")
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='majors',
                                help_text="Major Faculty")
    units = models.PositiveIntegerField(help_text="Major Units count")
    degree_level = models.CharField(max_length=20, choices=(
        ('AD', 'Associate\'s Degree'), ('BD', 'Bachelor\'s Degree'), ('MD', 'Master\'s Degree'),
        ('D', 'Doctorate or Ph.D.'),
        ('PD', 'Professional Degrees')),
                                    help_text="""Major's Degree Level ('AD', 'Associate\'s Degree'),
                    ('BD', 'Bachelor\'s Degree'), ('MD', 'Master\'s Degree'),
                    ('D', 'Doctorate or Ph.D.'),
                    ('PD', 'Professional Degrees')""")
