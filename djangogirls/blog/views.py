from django.shortcuts import render

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
        'post':post,
    }
    return render(request, 'blog/post_detail.html', context)

def post_add(request):
    if request.method == 'POST':
        return HttpResponse('POST request')
    elif request.method == 'GET':
        context = {

        }
        return render(request, 'blog/post_form.html', context)

# View(Controller) 구현
# post_detail 기능을 하는 함수를 구현
# 'post'라는 key로 Post.objects.first()에 해당하는 Post 객체를 전달
# 템플릿은 'blog/post_detail.html'을 사용

# Template(View) 구현
# 실제 템플릿 파일 생성
# 'post'라는 변수를 이용해 Post의 객체의 내용을 출력

# UrlResolver(urls.py)
# /post/detail/url을 'post_detail' 뷰와 연결
