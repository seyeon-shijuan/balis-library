from re import L
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from user_app.models import User
from datetime import datetime
# Create your views here.

def init(request) :
    user_id = request.session.get('user')
    # print("**************************************")
    # print(user_id)
    if user_id :
        user = User.objects.get(user_id = user_id)
        content = {'user' : user}
        return render(request, 'user_app/trends-main.html', content)
    return render(request, 'user_app/trends-main.html')

def join(request) :
    if request.method == 'POST' :
        context = {}
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']
        user_pwd = request.POST['user_pwd']
        check_pwd = request.POST['check_pwd']
        birthday = request.POST['birthday']
        
        isDup = User.objects.filter(user_id=user_id)
        if isDup.exists() :
            context['message'] = user_id +"가 중복됩니다."
            return render(request, 'user_app/join.html', context)

        else :
            if user_pwd == check_pwd :
                user = User(user_id=user_id, user_name=user_name, user_pwd=user_pwd, birthday=birthday, join_date=datetime.now())
                user.save()
                context['message'] = user_name +"님 회원 가입 되었습니다."
                return HttpResponseRedirect(reverse('user_app:login'))

            else :
                context['message'] = "password가 일치하지 않습니다."
                return render(request, 'user_app/join.html', context)

    elif request.method == 'GET' :
        return render(request, 'user_app/join.html')

def login(request) :
    if request.method == 'POST' :
        context = {}
        user_id = request.POST['user_id']
        user_pwd = request.POST['user_pwd']
        
        isDup = User.objects.filter(user_id=user_id)
        if isDup.exists() :
            checkUser = User.objects.get(user_id=user_id)
            if checkUser.user_pwd == user_pwd :
                request.session['user'] = checkUser.user_id
                context['message'] = checkUser.user_name + '님 반갑습니다.'
                return HttpResponseRedirect(reverse('user_app:home'))
                # return render(request, 'user_app/trends-main.html')
            else :
                context['message'] = "password가 일치하지 않습니다."
                return render(request, 'user_app/login.html', context)

        else :
            context['message'] = '일치하는 회원 정보가 없습니다.'
            return render(request, 'user_app/login.html', context)
                       
    elif request.method == 'GET' :
        return render(request, 'user_app/login.html')

def logout(request) :
    if request.session.get('user') :
        del(request.session['user'])
    return HttpResponseRedirect(reverse('user_app:login'))

def delete(request) :
    if request.method == 'GET' :
        return render(request, 'user_app/delete.html')
    else :
        user = request.session.get('user')
        context = {}
        delUser = User.objects.get(user_id = user)
        check_pwd = request.POST['user_pwd']
        if check_pwd == delUser.user_pwd :
            delUser.delete()
            logout(request)
            context['message'] = '탈퇴되었습니다.'
            return HttpResponseRedirect(reverse('user_app:login'))
        else :
            context['message'] = '비밀번호가 일치하지 않습니다.'
            return render(request, 'user_app/delete.html')


def update(request) :
    if request.method=='GET' :
        return render(request, 'user_app/update.html')
    else :
        context = {}
        user_id = request.session.get('user')
        user = User.objects.get(user_id=user_id)
        update_name = request.POST['user_name']
        update_pwd = request.POST['user_pwd']
        update_check_pwd = request.POST['check_pwd']
        update_bday = request.POST['birthday']

        if update_pwd == update_check_pwd :
            user.user_name = update_name
            user.user_pwd = update_pwd
            user.birthday = update_bday
            user.save()
            context['message'] = '회원 정보가 변경되었습니다.'
            return HttpResponseRedirect(reverse('user_app:mypage'))
        else :
            context['message'] = '비밀번호가 일치하지 않습니다.'
            return render(request, 'user_app/update.html')
        

def mypage(request) :
    if request.method=='GET' :
        user_id = request.session.get('user')
        # print("**************************************")
        # print(user_id)
        if user_id :
            user = User.objects.get(user_id = user_id)
            content = {'user' : user}
            return render(request, 'user_app/mypage.html', content)

    else :
        context = {}
        return render(request, 'user_app/mypage.html')
        
        
