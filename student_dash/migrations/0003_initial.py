# Generated by Django 4.2.10 on 2024-03-23 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('student_dash', '0002_initial'),
        ('university', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student'),
        ),
        migrations.AddField(
            model_name='studentcourse',
            name='term_taken',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university.semester'),
        ),
        migrations.AddField(
            model_name='semesterwithdrawalrequest',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university.semester'),
        ),
        migrations.AddField(
            model_name='semesterwithdrawalrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
        migrations.AddField(
            model_name='reconsiderationrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university.approvedcourse'),
        ),
        migrations.AddField(
            model_name='reconsiderationrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
        migrations.AddField(
            model_name='emergencywithdrawalrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university.approvedcourse'),
        ),
        migrations.AddField(
            model_name='emergencywithdrawalrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
        migrations.AddField(
            model_name='defermentrequest',
            name='academic_semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='university.semester'),
        ),
        migrations.AddField(
            model_name='defermentrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
        migrations.AddField(
            model_name='courseregistrationrequest',
            name='requested_courses',
            field=models.ManyToManyField(blank=True, related_name='course_request', to='university.approvedcourse'),
        ),
        migrations.AddField(
            model_name='courseregistrationrequest',
            name='requesting_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='added_courses',
            field=models.ManyToManyField(related_name='added_by', to='university.approvedcourse'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='dropped_courses',
            field=models.ManyToManyField(related_name='dropped_by', to='university.approvedcourse'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.student'),
        ),
    ]
