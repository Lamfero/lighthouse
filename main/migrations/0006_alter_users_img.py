# Generated by Django 4.0.5 on 2022-06-13 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_delete_secretkeys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='img',
            field=models.ImageField(upload_to='users'),
        ),
    ]