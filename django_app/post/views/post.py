from django.shortcuts import render, redirect

from post.forms import CommentForm, PostForm
from post.models import Post, Comment

__all__ = (
    'post_list',
    'post_detail',
    'post_like_toggle',
    'post_add',
    'post_delete',
)


def post_list(request):
    posts = Post.objects.filter(is_visible=True)
    # posts = Post.visible.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_id):
    # 인자로 전달된 post_id와 일치하는 id를 가진 Post객체 하나만 조회
    post = Post.objects.get(id=post_id)
    # Comment를 생성할 Form객체를 생성, 할당
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post_detail.html', context)


def post_add(request):
    def create_post_comment(file, comment_content):
        post = Post(author=request.user, photo=file)
        post.save()
        if comment_content != '':
            post.add_comment(user=request.user, content=comment_content)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('photo')
            comment_content = form.cleaned_data.get('content', '').strip()

            for file in files:
                create_post_comment(file, comment_content)

            return redirect('post:list')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'post/post_add.html', context)


def post_delete(request, post_id, db_delete=False):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if post.author.id == request.user.id:
            if db_delete:
                post.delete()
            else:
                post.is_visible = False
                post.save()

        return redirect('post:list')


def post_like_toggle(request, post_id):
    """
    1. post_detail.html에 form을 하나 더 생성
    2. 요청 view(url)가 post_like가 되도록 함
    3. 요청을 받은 후 적절히 PostLike처리
    4. redirect
    """
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.toggle_like(user=request.user)
        return redirect('post:list')