from django.db import models


class StudentCourse(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE, related_name='student_courses')
    grade = models.FloatField()

    def is_passed(self):
        if self.grade >= 10:
            return True
        else:
            return False

    def course_status(self):
        return 'In Progress' if self.course.semester.is_active() else 'Passed'


class CourseRegistrationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='registration_requests')
    courses = models.ManyToManyField('university.SemesterCourse', related_name='registration_requests')
    status = models.BooleanField(default=False)


class CourseCorrectionRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='correction_requests')
    dropped_courses = models.ManyToManyField('university.SemesterCourse', related_name='correction_drop_requests')
    added_courses = models.ManyToManyField('university.SemesterCourse', related_name='correction_add_requests')
    status = models.BooleanField(default=False)


class ReconsiderationRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='reconsideration_requests')
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='reconsideration_requests')
    status = models.BooleanField(default=False)
    text = models.TextField()
    response = models.TextField()


class EmergencyWithdrawalRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='emergency_withdrawal_requests')
    course = models.ForeignKey('university.SemesterCourse', on_delete=models.CASCADE,
                               related_name='emergency_withdrawal_requests')
    status = models.BooleanField(default=False)
    text = models.TextField()
    response = models.TextField()


class SemesterWithdrawalRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='semester_withdrawal_requests')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE,
                                 related_name='semester_withdrawal_requests')
    status = models.BooleanField(default=False)
    text = models.TextField()
    response = models.TextField()
    count_semester = models.BooleanField(default=False)


class DefermentRequest(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='deferment_requests')
    file = models.FileField(upload_to='deferment_files')
    semester = models.ForeignKey('university.Semester', on_delete=models.CASCADE,
                                 related_name='deferment_requests')
    faculty = models.ForeignKey('university.Faculty', on_delete=models.CASCADE,
                                related_name='deferment_requests')
