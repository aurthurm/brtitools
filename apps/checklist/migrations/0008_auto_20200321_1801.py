# Generated by Django 3.0.4 on 2020-03-21 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0007_auto_20200320_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='has_sub_questions',
        ),
        migrations.RemoveField(
            model_name='question',
            name='has_sub_questions_grouped',
        ),
    ]
