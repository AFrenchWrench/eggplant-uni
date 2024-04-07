from django.db import models


# Create your models here.
class AbstractBaseRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                related_name='%(app_label)s_%(class)s_related', null=True,
                                help_text='Request To Student Relation')

    class Meta:
        abstract = True


class AbstractRequest(AbstractBaseRequest):
    status = models.CharField(max_length=1, choices=(('A', 'Accepted'), ('R', 'Rejected'), ('I', 'In Progress'),),
                              default='I',
                              help_text="Request Status ('A', 'Accepted'), ('R', 'Rejected'), ('I', 'In Progress')")

    class Meta:
        abstract = True


class CourseRegistrationRequest(AbstractRequest):
    courses = models.ManyToManyField('university.SemesterCourse', related_name='registration_requests',
                                     through='StudentCourseParticipant', help_text='Request To Courses Relation')


class StudentCourseParticipant(models.Model):
    student = models.ForeignKey('CourseRegistrationRequest', on_delete=models.CASCADE,
                                related_name='student_semester_course', help_text='Request To Student Relation')
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='student_semester_course', help_text='Request To Courses Relation')
    status = models.CharField(max_length=1,
                              choices=(('R', 'Registered'), ('A', 'Added'), ('D', 'Dropped'), ('I', 'In Progress'),),
                              default='I',
                              help_text="Request Status ('A', 'Accepted'), ('R', 'Rejected'), ('I', 'In Progress')")


class CourseCorrectionRequest(AbstractRequest):
    dropped_courses = models.ManyToManyField('university.SemesterCourse', related_name='correction_drop_requests',
                                             help_text='Request To Courses Relation')
    added_courses = models.ManyToManyField('university.SemesterCourse', related_name='correction_add_requests',
                                           help_text='Request To Courses Relation')


class ReconsiderationRequest(AbstractRequest):
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='reconsideration_requests', null=True,
                               help_text='Request To Courses Relation')
    text = models.TextField(help_text='Request Text')
    response = models.TextField(help_text='Response Text')


class EmergencyWithdrawalRequest(AbstractRequest):
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='emergency_withdrawal_requests', null=True,
                               help_text='Request To Courses Relation')
    text = models.TextField(help_text='Request Text')
    response = models.TextField(help_text='Response Text')


class SemesterWithdrawalRequest(AbstractRequest):
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE,
                                 related_name='semester_withdrawal_requests', null=True,
                                 help_text='Request To Semester Relation')
    text = models.TextField(help_text='Request Text')
    response = models.TextField(help_text='Response Text')
    count_semester = models.BooleanField(default=False, help_text='Whether To Count Semesters Or Not')


class DefermentRequest(AbstractBaseRequest):
    file = models.FileField(upload_to='deferment_files', help_text='Request File')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE,
                                 related_name='deferment_requests', null=True, help_text='Request To Semester Relation')
    faculty = models.ForeignKey('university.Faculty', on_delete=models.CASCADE,
                                related_name='deferment_requests', null=True, help_text='Request To Faculty Relation')
