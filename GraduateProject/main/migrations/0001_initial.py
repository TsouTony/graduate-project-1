# Generated by Django 2.2.6 on 2019-11-07 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.otherFunctions.listField
import main.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('img_url', models.ImageField(null=True, storage=main.storage.ImageStorage(), upload_to='img')),
                ('cmpScore', models.IntegerField(null=True)),
                ('like', models.FloatField(null=True)),
                ('description', models.TextField(null=True)),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('label', main.otherFunctions.listField.ListField(null=True, token=',')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imgs', to=settings.AUTH_USER_MODEL)),
                ('user_like', models.ManyToManyField(null=True, related_name='like_imgs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('createTime', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.Img')),
            ],
        ),
    ]
