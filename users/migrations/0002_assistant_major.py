# Generated by Django 4.2.10 on 2024-04-04 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assistant',
            name='major',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assistants', to='university.major'),
            preserve_default=False,
        ),
    ]
