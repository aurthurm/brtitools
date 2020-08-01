# Generated by Django 3.0.4 on 2020-03-22 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0012_auto_20200322_0706'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='answer',
            name='unique answer',
        ),
        migrations.AddConstraint(
            model_name='answer',
            constraint=models.UniqueConstraint(fields=('question', 'response'), name='unique answer'),
        ),
    ]
