# Generated by Django 3.0.4 on 2020-03-17 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0004_auto_20200317_0721'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='help',
            field=models.TextField(blank=True, null=True, verbose_name='Help'),
        ),
    ]
