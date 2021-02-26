from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Account

# Create your views here.

# 회원가입
def signup(request):
    if request.method=='POST':
        # 빈칸이 아니면
        if request.POST['name'] != '' and request.POST['id'] != '' and request.POST['pw1'] != '':
            # 중복 아이디 확인
            if Account.objects.filter(acc_id = request.POST['id']).exists():
                return render(request, "signup.html", {'message': '❗ 중복 id 존재!'})
            else:
                # 비밀번호 확인 되었을 때 가입 성공
                if request.POST['pw1'] == request.POST['pw2']:
                    account = Account(acc_id = request.POST['id'], acc_pw = request.POST['pw1'], acc_name=request.POST['name'])
                    account.save()
                    return redirect('home')
                # 비밀번호 확인 안됨
                else:
                    return render(request, "signup.html", {'message': '❗ [비밀번호]와 [비밀번호 확인] 값이 일치하지 않습니다!'})
        # 빈칸이 하나라도 있으면
        else:
            return render(request, "signup.html", {'message': '❗ 모든 항목은 필수 입력값입니다!'})
    return render(request, "signup.html")

# 아이디 중복 확인

# 로그인
def login(request):
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pw']

        if Account.objects.filter(acc_id = id).exists():
            if Account.objects.filter(acc_pw = pw).exists():
                request.session['user'] = id
                return redirect('home')
        return render(request, "login.html", {'message':'❗ ID/PW 오류입니다. 다시 시도해 주세요.'})

    return render(request, "login.html")

# 로그아웃
def logout(request):
    request.session.clear()
    return redirect('home')