# Generated by Django 4.2.10 on 2024-03-25 00:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('university', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semesterstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_students', to='users.student'),
        ),
        migrations.AddField(
            model_name='semestercourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_courses', to='university.course'),
        ),
        migrations.AddField(
            model_name='semestercourse',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_courses', to='users.professor'),
        ),
        migrations.AddField(
            model_name='semestercourse',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='semester_courses', to='university.semester'),
        ),
        migrations.AddField(
            model_name='major',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='majors', to='university.faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='corequisites',
            field=models.ManyToManyField(blank=True, related_name='corequisite_for', to='university.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='university.faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(blank=True, related_name='prerequisite_for', to='university.course'),
        ),
    ]
