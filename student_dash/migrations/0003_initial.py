# Generated by Django 4.2.10 on 2024-03-25 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student_dash', '0002_initial'),
        ('university', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='users.student'),
        ),
        migrations.AddField(
            model_name='semesterwithdrawalrequest',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_withdrawal_requests', to='university.semester'),
        ),
        migrations.AddField(
            model_name='semesterwithdrawalrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_withdrawal_requests', to='users.student'),
        ),
        migrations.AddField(
            model_name='reconsiderationrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reconsideration_requests', to='university.semestercourse'),
        ),
        migrations.AddField(
            model_name='reconsiderationrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reconsideration_requests', to='users.student'),
        ),
        migrations.AddField(
            model_name='emergencywithdrawalrequest',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_withdrawal_requests', to='university.semestercourse'),
        ),
        migrations.AddField(
            model_name='emergencywithdrawalrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emergency_withdrawal_requests', to='users.student'),
        ),
        migrations.AddField(
            model_name='defermentrequest',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deferment_requests', to='university.faculty'),
        ),
        migrations.AddField(
            model_name='defermentrequest',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deferment_requests', to='university.semester'),
        ),
        migrations.AddField(
            model_name='defermentrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deferment_requests', to='users.student'),
        ),
        migrations.AddField(
            model_name='courseregistrationrequest',
            name='courses',
            field=models.ManyToManyField(related_name='registration_requests', to='university.semestercourse'),
        ),
        migrations.AddField(
            model_name='courseregistrationrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_requests', to='users.student'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='added_courses',
            field=models.ManyToManyField(related_name='correction_add_requests', to='university.semestercourse'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='dropped_courses',
            field=models.ManyToManyField(related_name='correction_drop_requests', to='university.semestercourse'),
        ),
        migrations.AddField(
            model_name='coursecorrectionrequest',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='correction_requests', to='users.student'),
        ),
    ]
