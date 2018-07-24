# Generated by Django 2.0.7 on 2018-07-24 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=128)),
                ('size', models.IntegerField()),
                ('path', models.CharField(max_length=256)),
            ],
        ),
    ]
