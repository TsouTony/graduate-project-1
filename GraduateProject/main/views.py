import random
import time

from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render

from main.models import User, Img, Comment


# Create your views here.

def main(request):
    img = None
    isUploadImg = False
    randCmpScore = random.randint(5, 9)
    loginUserName = request.user.username
    if loginUserName is not None and loginUserName != '':
        loginUser = User.objects.get(username=loginUserName)

    if request.method == 'POST':
        imgID = time.strftime('%Y_%m_%d_%H_%M_%S_') + str(random.randint(10, 99))
        # img = Img(img_url=request.FILES.get('img'),author=request.user.username,computerScoure=cmpScore,like=0)
        img = Img(id=imgID, img_url=request.FILES.get('img'), author=loginUser, cmpScore=randCmpScore, like=0)
        img.save()
        isUploadImg = True
        img.cmpScore = assessPicture(str(img.img_url))
        img.label = getLabel(str(img.img_url))
        img.save()

    imgListOrderByCmpScore = Img.objects.order_by("-cmpScore")
    imgListOrderByLike = Img.objects.order_by("-like")
    currentImg = img
    context = {
        'imgListOrderByCmpScore': imgListOrderByCmpScore,
        'imgListOrderByLike': imgListOrderByLike,
        'currentImg': currentImg,
        'isUploadImg': isUploadImg,
    }

    return render(request, 'main/index.html', context)


def blog(request, user):
    user = User.objects.get(username=user)
    userImgList = user.imgs.all()
    context = {
        'user': user,
        'userImgList': userImgList
    }
    return render(request, 'blog/blog.html', context)


def imgDetail(request, user, imgID):
    # 用 if post 新增comments
    if request.method == 'POST':
        authorName = request.POST['author']
        author = User.objects.get(username=authorName)
        imgID = request.POST['img']
        currentImg = Img.objects.get(id=imgID)
        content = request.POST['content']
        commentID = time.strftime('%Y%m%d%H%M%S') + authorName
        comment = Comment(id=commentID, author=author, img=currentImg, content=content)
        comment.save()

    user = User.objects.get(username=user)
    img = Img.objects.get(id=imgID)
    commentList = img.comments.all()
    print(img.img_url.url)
    context = {
        'currentImg': img,
        'commentList': commentList
    }
    return render(request, 'blog/imgDetail.html', context)


def addComment(request):
    authorName = request.POST['author']
    author = User.objects.get(username=authorName)
    imgID = request.POST['imgID']
    currentImg = Img.objects.get(id=imgID)
    content = request.POST['content']
    comment = Comment(id='123', author=author, img=currentImg, content=content)
    comment.save()
    context = {
        'currentImg': currentImg,
    }

    return HttpResponseRedirect('/blog/' + authorName + '/' + imgID)


#return render(request, 'blog/imgDetail.html', context)

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/main/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_activate:
        auth.login(request, user)
        return HttpResponseRedirect('/main/')
    else:
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/main/')


def signUp(request):

    first_name = request.POST['firstName']
    last_name = request.POST['lastName']
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(
        username=username, password=password, first_name=first_name, last_name=last_name)
    user.save()

    return HttpResponseRedirect(reverse('main'))
