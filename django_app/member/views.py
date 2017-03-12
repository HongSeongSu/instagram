from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from member.forms import LoginForm, SignupForm, ChangeProfileImageModelForm, SignupModelForm
from post.models import Post


def logins(request):
    if request.method == 'POST':
        # LoginForm을 사용
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # 전달되어온 POST데이터에서 'username'과'password' 키의 값들을 사용
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate의 인자로 POST로 전달받은 username, password를 사용
            user = authenticate(username=username, password=password)

            # 만약 인증이 정상적으로 완료되었다면
            # ( 해당하는 username, password에 일치하는 User객체가 존재할 경우)
            if user is not None:
                # Django의 인증관리 시스템을 이용하여 세션을 관리해주기 위해 login()함수 사용
                login(request, user)
                return redirect('post:list')
            # 인증에 실패하였다면 (username, password에 일치하는 User객체가 존재하지 않을 경우)
            else:
                form.add_error(None, 'ID or Password incorrect')

    # GET method로 요청이 왔을 경우
    else:
        # 빈 LoginForm 객체를 생성
        form = LoginForm()

    context = {
        'form': form,
    }
    # member/login.html 템플릿을 render한 결과를 리턴
    return render(request, 'member/login.html', context)


def signup_fbv(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            login(request, user)
            return redirect('post:list')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'member/signup.html', context)


def singup_model_form_fbv(request):
    if request.method == 'POST':
        form = SignupModelForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post:list')
        else:
            form = SignupModelForm()
        context = {
            'form': form,
        }
        return render(request, 'member/signup.html', context)


@login_required
def profile(request):
    post_count = Post.objects.filter(author=request.user).count()
    follower_count = request.user.follower_set.count()
    following_count = request.user.following.count()
    context = {
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
    }
    return render(request, 'member/profile.html', context)


@login_required
def change_profile_image(request):
    if request.method == 'POST':
        form = ChangeProfileImageModelForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES

        )
        if form.is_valid():
            form.save()
            return redirect('member:profile')
    else:
        form = ChangeProfileImageModelForm(instance=request.user)
        context = {
            'form': form,
        }
        return render(request, 'member/change_profile_image.html', context)


def logout_view(request):
    logout(request)
    return redirect('member:login')

# def logout_fbv(request):
#     logout(request)
#     return redirect('member:login')
