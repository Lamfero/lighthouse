# Generated by Django 4.1 on 2022-09-03 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creating_project', '0007_alter_creatingproject_file_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatingproject',
            name='currency',
            field=models.CharField(default='$', max_length=10),
        ),
    ]