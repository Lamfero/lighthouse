# Generated by Django 4.0.5 on 2022-07-05 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_orders_completed_on_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='completed_on_time',
            field=models.CharField(max_length=10, null=True),
        ),
    ]