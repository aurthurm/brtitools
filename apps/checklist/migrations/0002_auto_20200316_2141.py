# Generated by Django 3.0.4 on 2020-03-16 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number'),
        ),
    ]
