# Generated by Django 3.0.4 on 2020-03-16 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'site',
                'verbose_name_plural': 'sites',
            },
        ),
    ]
