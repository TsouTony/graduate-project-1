from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User
from .storage import ImageStorage
from .otherFunctions.listField import ListField


# Create your models here.
# QuerySet 語法 - all()， get()， filter() 和 exclude()

class UserProfile(models.Model):
    # auth User default field
    # username
    # password
    # first_name
    # last_name
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # follow user
    # is_authenticated

    def __str__(self):
        return self.user.username


class Img(models.Model):
    # 每張img要有自己的id
    id = models.CharField(primary_key=True, max_length=20, null=False)
    img_url = models.ImageField(null=True, upload_to='img', storage=ImageStorage())
    cmpScore = models.FloatField(null=True)
    like = models.IntegerField(null=True)
    description = models.TextField(null=True)
    createTime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imgs')
    user_like = models.ManyToManyField(User, related_name="like_imgs", null=True)
    label = ListField(null=True)

    def __str__(self):
        return self.id


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    content = models.TextField()
    createTime = models.DateTimeField(auto_now=True)
    img = models.ForeignKey(Img, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.id



