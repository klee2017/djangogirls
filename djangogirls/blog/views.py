from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

User = get_user_model()

from .models import Post


def post_list(request):
    # post_list view가 published_date가 존재하는 Post목록만 보여주도록
    posts = Post.objects.all()
    context = {
        # posts key의 value는 QuerySet
        'posts': posts,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    # Post 인스턴스 1개만 가져옴, 변수명 post

    # get에 실패했을 때
    # HTTP로 문자열을 돌려주려면
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse('No Post', status=404)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)


def post_add(request):
    # post_list.html에 post_add로 갈 수 있는 버튼링크 추가 ({% url %}태그 사용해서 동적으로 구성)
    #
    # post_form.html에 checkbox를 추가
    #   이를 이용해서 publish여부를 결정
    #
    # Post생성 완료 후(DB에 저장 후), post_list페이지로 이동
    #   https://docs.djangoproject.com/ko/1.11/topics/http/shortcuts/#redirect
    #    extra) 작성한 Post에 해당하는 post_detail페이지로 이동
    #
    # Post생성시 Post.objects.create()메서드 사용
    #
    # extra) Post delete기능 구현
    #   def post_delete(request, pk):
    #       (POST요청에서만 동작해야함)
    #       -> pk에 해당하는 Post를 삭제하고, post_list페이지로 이동

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_publish = bool(request.POST.get('is_publish'))
        author = User.objects.get(username='kay')

        if title and content:
            post = Post.objects.create(
                author=author,
                title=title,
                content=content,
            )
            if is_publish:
                post.publish()
            else:
                post.save()
            return redirect('post_detail', pk=post.pk)

        context = {
            'title':title,
            'content':content,
        }

    else:
        context = {}

    return render(request, 'blog/post_form.html', context)
            # request.POST에서 'title', 'content'키에 해당하는 value를 받아
            # 새 Post 객체 생성
            # 생성 후에 해당 객체의 title, content를 HttpResponse로 전달

            # title이나 content값이 오지 않았을 경우에는 객체를 생성하지 않고 다시 작성페이지로 이동

# View(Controller) 구현
# post_detail 기능을 하는 함수를 구현
# 'post'라는 key로 Post.objects.first()에 해당하는 Post 객체를 전달
# 템플릿은 'blog/post_detail.html'을 사용

# Template(View) 구현
# 실제 템플릿 파일 생성
# 'post'라는 변수를 이용해 Post의 객체의 내용을 출력

# UrlResolver(urls.py)
# /post/detail/url을 'post_detail' 뷰와 연결

def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('post_list')
    else:
        return HttpResponse('Permission denied', status=403)