# Generated by Django 4.1 on 2022-08-31 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_project_file_1_project_file_2_project_file_3_and_more'),
        ('creating_project', '0006_alter_creatingproject_enable_price_upper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatingproject',
            name='file_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creating_project_file_1', to='main.projectfiles'),
        ),
        migrations.AlterField(
            model_name='creatingproject',
            name='file_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creating_project_file_2', to='main.projectfiles'),
        ),
        migrations.AlterField(
            model_name='creatingproject',
            name='file_3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creating_project_file_3', to='main.projectfiles'),
        ),
        migrations.AlterField(
            model_name='creatingproject',
            name='file_4',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creating_project_file_4', to='main.projectfiles'),
        ),
        migrations.AlterField(
            model_name='creatingproject',
            name='file_5',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creating_project_file_5', to='main.projectfiles'),
        ),
    ]
