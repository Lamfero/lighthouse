# Generated by Django 4.0.5 on 2022-06-10 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('date_birth', models.DateField()),
                ('desctiption', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('subcategories', models.CharField(max_length=200)),
                ('interests', models.CharField(max_length=400)),
                ('portfolio', models.CharField(max_length=500)),
                ('secret_key', models.CharField(max_length=50)),
                ('img', models.ImageField(height_field=100, upload_to='users', width_field=100)),
            ],
        ),
    ]
