# Generated by Django 5.1.4 on 2025-01-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imfapp', '0002_login_usertype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='usertype',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
