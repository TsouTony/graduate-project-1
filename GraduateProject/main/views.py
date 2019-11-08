import random
import time

from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from main.models import User, Img, Comment
from .otherFunctions.visionAPI import getLabel
from .otherFunctions.score_mobilenet_input import assessPicture


# Create your views here.

def main(request):
    if request.user.is_authenticated:
        username = request.user.username
        loginUser = User.objects.get(username=username)

    img = None
    isUploadImg = False
    randCmpScore = random.randint(5, 9)
    loginUserName = request.user.username
    if loginUserName is not None and loginUserName != '':
        loginUser = User.objects.get(username=loginUserName)

    if request.method == 'POST':
        imgID = time.strftime('%Y%m%d%H%M%S') + str(random.randint(10, 99))
        description = request.POST.get('description', '')
        print('des' + description)
        img = Img(id=imgID, img_url=request.FILES.get('img'), author=loginUser, cmpScore=randCmpScore, like=0, description=description)
        img.save()
        img.cmpScore = assessPicture(str(img.img_url))
        img.label = getLabel(str(img.img_url))
        img.save()
        isUploadImg = True

    imgListOrderByCmpScore = Img.objects.order_by("-cmpScore")
    imgListOrderByLike = Img.objects.order_by("-like")
    currentImg = img
    context = {
        'imgListOrderByCmpScore': imgListOrderByCmpScore,
        'imgListOrderByLike': imgListOrderByLike,
        'currentImg': currentImg,
        'isUploadImg': isUploadImg
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
    if request.user.is_authenticated:
        username = request.user.username
        loginUser = User.objects.get(username=username)

    img = Img.objects.get(id=imgID)
    commentList = img.comments.all()
    imgListOrderByCmpScore = Img.objects.order_by("-cmpScore")
    imgListOrderByLike = Img.objects.order_by("-like")
    context = {
        'currentImg': img,
        'commentList': commentList,
        'isLike': loginUser.like_imgs.filter(id=img.id).exists(),
        'imgListOrderByCmpScore': imgListOrderByCmpScore,
        'imgListOrderByLike': imgListOrderByLike
    }
    return render(request, 'blog/imgDetail.html', context)


# def addComment(request):
#     authorName = request.POST['author']
#     author = User.objects.get(username=authorName)
#     imgID = request.POST['imgID']
#     currentImg = Img.objects.get(id=imgID)
#     content = request.POST['content']
#     comment = Comment(id='123', author=author, img=currentImg, content=content)
#     comment.save()
#     context = {
#         'currentImg': currentImg,
#     }
#
#     return HttpResponseRedirect('/blog/' + authorName + '/' + imgID)


# return render(request, 'blog/imgDetail.html', context)

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_activate:
        request.session['username'] = username
        auth.login(request, user)
        return HttpResponseRedirect('/main/')
    else:
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/main/')


def signUp(request):
    if request.method == 'POST':
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        username = request.POST['account']
        password = request.POST['password']
        checkPassword = request.POST['checkPassword']
        if password == checkPassword:
            user = User.objects.create_user(
                username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return HttpResponseRedirect('/main/')
        else:
            return HttpResponseRedirect('/signUp/')

    return render(request, 'registration/signUp.html')


def ajax_like(request):
    username = request.GET['username']
    imgID = request.GET['imgID']
    user = User.objects.get(username=username)
    img = Img.objects.get(id=imgID)
    isLike = False

    if img.user_like.filter(username=username).exists():
        img.user_like.remove(user)
        likeScore = img.like
        img.like = likeScore - 1
    else:
        img.user_like.add(user)
        likeScore = img.like
        img.like = likeScore + 1
        isLike = True

    img.save()

    data = {
        'like-score': img.like,
        'isLike': isLike
    }

    return JsonResponse(data)


def ajax_comment(request):
    username = request.GET['username']
    imgID = request.GET['imgID']
    content = request.GET['content']
    user = User.objects.get(username=username)
    currentImg = Img.objects.get(id=imgID)
    commentID = time.strftime('%Y%m%d%H%M%S') + username
    comment = Comment(id=commentID, author=user, img=currentImg, content=content)
    comment.save()

    data = {
        'author': username,
        'content': content
    }

    return JsonResponse(data)
