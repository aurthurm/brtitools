# Generated by Django 3.0.4 on 2020-03-22 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0008_auto_20200321_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Comment'),
        ),
    ]
