# Generated by Django 4.2.10 on 2024-04-04 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='faculty',
        ),
        migrations.AddField(
            model_name='course',
            name='major',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='university.major'),
            preserve_default=False,
        ),
    ]
