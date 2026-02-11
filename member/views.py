
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from member.models import Profile

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        address = request.POST.get('address', '').strip()

        # -------------------------
        # 1. 유효성 검사
        # -------------------------
        errors = {}

        if not name:
            errors['name'] = "이름을 입력하세요."

        if not email:
            errors['email'] = "이메일을 입력하세요."
        elif User.objects.filter(username=email).exists():
            errors['email'] = "이미 존재하는 이메일입니다."

        if not password:
            errors['password'] = "비밀번호를 입력하세요."

        if not address:
            errors['address'] = "주소를 입력하세요."

        # 오류 있으면 다시 폼으로 반환
        if errors:
            return render(request, 'member/signup.html', {
                'errors': errors,
                'name': name,
                'email': email,
                'address': address
            })

        # -------------------------
        # 2. 회원 생성(User 저장)
        # -------------------------
        user = User.objects.create_user(
            username=email,          # ID 대용
            email=email,             # 이메일 저장
            password=password,       # 비밀번호는 자동으로 해싱됨
            first_name=name          # 이름 저장
        )

        # -------------------------
        # 3. 자동 생성된 Profile 가져와서 address 저장
        # -------------------------
        profile = Profile.objects.get(user=user)  # signals에서 이미 생성돼 있음
        profile.address = address
        profile.save()

        messages.success(request, "회원 가입 성공! 로그인 해주세요.")
        return redirect('member:login')

    # GET 요청
    return render(request, 'member/signup.html')


from django.contrib.auth import authenticate, login
from .forms import LoginForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # username=email 방식으로 인증
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/home')  # 로그인 성공
            else:
                messages.error(request, "이메일 또는 비밀번호가 올바르지 않습니다.")
    else:
        form = LoginForm()

    return render(request, 'member/login.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # 세션 삭제 + 로그아웃 처리
    messages.success(request, "로그아웃 되었습니다.")
    return redirect('/home')  # 로그아웃 후 이동할 주소