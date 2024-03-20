import uuid

from django.db import models


# Create your models here.


class StudentCourse(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('university.ApprovedCourse', on_delete=models.PROTECT)
    course_status = models.CharField(max_length=20)
    grade = models.FloatField()
    term_taken = models.ForeignKey('university.Semester', on_delete=models.PROTECT)


class CourseRegistrationRequest(models.Model):
    request_code = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=16, editable=False)
    requesting_student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    requested_courses = models.ManyToManyField('university.ApprovedCourse', related_name='course_request', blank=True)
    approval_status = models.CharField(max_length=20)


class CourseCorrectionRequest(models.Model):
    request_code = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=16, editable=False)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    dropped_courses = models.ManyToManyField('university.ApprovedCourse', related_name='dropped_by')
    added_courses = models.ManyToManyField('university.ApprovedCourse', related_name='added_by')
    approval_status = models.CharField(max_length=20)


class ReconsiderationRequest(models.Model):
    request_code = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=16, editable=False)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    course = models.ForeignKey('university.ApprovedCourse', on_delete=models.PROTECT)
    reconsideration_text = models.TextField()
    reconsideration_response = models.TextField()


class EmergencyWithdrawalRequest(models.Model):
    request_code = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=16, editable=False)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    course = models.ForeignKey('university.ApprovedCourse', on_delete=models.PROTECT)
    request_outcome = models.CharField(max_length=20)
    student_explanation = models.TextField()
    educational_deputy_explanation = models.TextField()


class SemesterWithdrawalRequest(models.Model):
    request_code = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=16, editable=False)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    semester = models.ForeignKey('university.Semester', on_delete=models.PROTECT)
    withdrawal_outcome = models.CharField(max_length=50)
    student_explanation = models.TextField()
    educational_deputy_explanation = models.TextField()


class DefermentRequest(models.Model):
    request_code = models.UUIDField(primary_key=True, default=uuid.uuid4, max_length=16, editable=False)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    deferment_file = models.FileField(upload_to='deferment_files')
    academic_semester = models.ForeignKey('university.Semester', on_delete=models.PROTECT)
    issuing_authority = models.CharField(max_length=100)
