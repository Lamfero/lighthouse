# Generated by Django 4.0.5 on 2022-07-03 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_orders_rating_orders_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_employee', to='main.users'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_employer', to='main.users'),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purpose', models.TextField(null=True)),
                ('price', models.CharField(max_length=50, null=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_epmloyee', to='main.users')),
                ('employer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_epmloyer', to='main.users')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servise', to='main.service'),
        ),
    ]
