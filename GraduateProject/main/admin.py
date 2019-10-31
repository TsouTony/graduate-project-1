from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Img, Comment

# Register your models here.
class adminIMG(admin.ModelAdmin):
    list_display = ('img_url','createTime','cmpScore','author','label')
admin.site.register(Img,adminIMG)

class adminCOMMENT(admin.ModelAdmin):
    list_display = ('author','img','createTime','content')
admin.site.register(Comment,adminCOMMENT) 