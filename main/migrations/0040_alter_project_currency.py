# Generated by Django 4.1 on 2022-09-03 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_project_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='currency',
            field=models.CharField(max_length=10),
        ),
    ]
