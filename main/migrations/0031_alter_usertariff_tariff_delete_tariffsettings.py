# Generated by Django 4.0.5 on 2022-07-06 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tariffs', '0001_initial'),
        ('main', '0030_tariffsettings_usertariff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertariff',
            name='tariff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='name_tariff', to='tariffs.tariffsettings'),
        ),
        migrations.DeleteModel(
            name='TariffSettings',
        ),
    ]
