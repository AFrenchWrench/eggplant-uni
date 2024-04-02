from django.db import models


# Create your models here.
class AbstractBaseRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE,
                                related_name='%(app_label)s_%(class)s_related', null=True)

    class Meta:
        abstract = True


class AbstractRequest(AbstractBaseRequest):
    status = models.CharField(max_length=1, choices=(('A', 'Accepted'), ('R', 'Rejected'), ('I', 'In Progress'),),
                              default='I')

    class Meta:
        abstract = True


class CourseRegistrationRequest(AbstractRequest):
    courses = models.ManyToManyField('university.SemesterCourse', related_name='registration_requests',
                                     through='StudentCourseParticipant')


class StudentCourseParticipant(models.Model):
    student = models.ForeignKey('CourseRegistrationRequest', on_delete=models.CASCADE,
                                related_name='student_semester_course')
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='student_semester_course')
    status = models.CharField(max_length=1,
                              choices=(('R', 'Registered'), ('A', 'Added'), ('D', 'Dropped'), ('I', 'In Progress'),),
                              default='I')


class CourseCorrectionRequest(AbstractRequest):
    dropped_courses = models.ManyToManyField('university.SemesterCourse', related_name='correction_drop_requests')
    added_courses = models.ManyToManyField('university.SemesterCourse', related_name='correction_add_requests')


class ReconsiderationRequest(AbstractRequest):
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='reconsideration_requests', null=True)
    text = models.TextField()
    response = models.TextField()


class EmergencyWithdrawalRequest(AbstractRequest):
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='emergency_withdrawal_requests', null=True)
    text = models.TextField()
    response = models.TextField()


class SemesterWithdrawalRequest(AbstractRequest):
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE,
                                 related_name='semester_withdrawal_requests', null=True)
    text = models.TextField()
    response = models.TextField()
    count_semester = models.BooleanField(default=False)


class DefermentRequest(AbstractBaseRequest):
    file = models.FileField(upload_to='deferment_files')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE,
                                 related_name='deferment_requests', null=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.CASCADE,
                                related_name='deferment_requests', null=True)
