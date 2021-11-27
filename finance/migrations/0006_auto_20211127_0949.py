# Generated by Django 3.2.9 on 2021-11-27 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_auto_20211126_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_type',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_status',
            field=models.CharField(choices=[('s', 'SUCCESSFUL'), ('p', 'PENDING')], default='p', max_length=15),
        ),
    ]
