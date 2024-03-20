# Generated by Django 5.0.3 on 2024-03-20 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_initial'),
        ('users', '0002_alter_studentcourse_options'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseOffering',
            new_name='SemesterCourse',
        ),
        migrations.RemoveField(
            model_name='courseregistrationrequest',
            name='requested_courses',
        ),
        migrations.RemoveField(
            model_name='courseregistrationrequest',
            name='requesting_student',
        ),
        migrations.RemoveField(
            model_name='defermentrequest',
            name='academic_semester',
        ),
        migrations.RemoveField(
            model_name='defermentrequest',
            name='student',
        ),
        migrations.RemoveField(
            model_name='emergencywithdrawalrequest',
            name='course',
        ),
        migrations.RemoveField(
            model_name='emergencywithdrawalrequest',
            name='student',
        ),
        migrations.RemoveField(
            model_name='reconsiderationrequest',
            name='course',
        ),
        migrations.RemoveField(
            model_name='reconsiderationrequest',
            name='student',
        ),
        migrations.RemoveField(
            model_name='semesterwithdrawalrequest',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='semesterwithdrawalrequest',
            name='student',
        ),
        migrations.DeleteModel(
            name='CourseCorrectionRequest',
        ),
        migrations.DeleteModel(
            name='CourseRegistrationRequest',
        ),
        migrations.DeleteModel(
            name='DefermentRequest',
        ),
        migrations.DeleteModel(
            name='EmergencyWithdrawalRequest',
        ),
        migrations.DeleteModel(
            name='ReconsiderationRequest',
        ),
        migrations.DeleteModel(
            name='SemesterWithdrawalRequest',
        ),
    ]