from django.db import models

from users.utils import generate_code


class StudentCourse(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('university.ApprovedCourse', on_delete=models.PROTECT)
    course_status = models.CharField(max_length=20)
    grade = models.FloatField()
    term_taken = models.ForeignKey('university.Semester', on_delete=models.PROTECT)


class CourseRegistrationRequest(models.Model):
    request_code = models.CharField(default=generate_code, max_length=10, editable=False, unique=True)
    requesting_student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    requested_courses = models.ManyToManyField('university.ApprovedCourse', related_name='course_request', blank=True)
    approval_status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = generate_code()
        super(CourseRegistrationRequest, self).save(*args, **kwargs)


class CourseCorrectionRequest(models.Model):
    request_code = models.CharField(default=generate_code, max_length=10, editable=False, unique=True)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    dropped_courses = models.ManyToManyField('university.ApprovedCourse', related_name='dropped_by')
    added_courses = models.ManyToManyField('university.ApprovedCourse', related_name='added_by')
    approval_status = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = generate_code()
        super(CourseCorrectionRequest, self).save(*args, **kwargs)


class ReconsiderationRequest(models.Model):
    request_code = models.CharField(default=generate_code, max_length=10, editable=False, unique=True)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    course = models.ForeignKey('university.ApprovedCourse', on_delete=models.PROTECT)
    reconsideration_text = models.TextField()
    reconsideration_response = models.TextField()

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = generate_code()
        super(ReconsiderationRequest, self).save(*args, **kwargs)


class EmergencyWithdrawalRequest(models.Model):
    request_code = models.CharField(default=generate_code, max_length=10, editable=False, unique=True)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    course = models.ForeignKey('university.ApprovedCourse', on_delete=models.PROTECT)
    request_outcome = models.CharField(max_length=20)
    student_explanation = models.TextField()
    educational_deputy_explanation = models.TextField()

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = generate_code()
        super(EmergencyWithdrawalRequest, self).save(*args, **kwargs)


class SemesterWithdrawalRequest(models.Model):
    request_code = models.CharField(default=generate_code, max_length=10, editable=False, unique=True)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    semester = models.ForeignKey('university.Semester', on_delete=models.PROTECT)
    withdrawal_outcome = models.CharField(max_length=50)
    student_explanation = models.TextField()
    educational_deputy_explanation = models.TextField()

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = generate_code()
        super(SemesterWithdrawalRequest, self).save(*args, **kwargs)


class DefermentRequest(models.Model):
    request_code = models.CharField(default=generate_code, max_length=10, editable=False, unique=True)
    student = models.ForeignKey('users.Student', on_delete=models.PROTECT)
    deferment_file = models.FileField(upload_to='deferment_files')
    academic_semester = models.ForeignKey('university.Semester', on_delete=models.PROTECT)
    issuing_authority = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.request_code:
            self.request_code = generate_code()
        super(DefermentRequest, self).save(*args, **kwargs)
