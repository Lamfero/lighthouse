# Generated by Django 4.0.5 on 2022-06-28 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_users_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='img',
            field=models.ImageField(upload_to='images/users/'),
        ),
    ]