# Generated by Django 4.0.5 on 2022-06-13 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_users_category_alter_users_date_birth_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecretKeys',
            fields=[
                ('telegram_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.users')),
                ('secret_key', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
