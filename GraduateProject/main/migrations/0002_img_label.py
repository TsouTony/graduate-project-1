# Generated by Django 2.2.6 on 2019-10-24 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='img',
            name='label',
            field=models.TextField(null=True),
        ),
    ]
