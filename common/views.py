# views.py 회원가입 부분 예시
from .forms import UserForm
from .models import Profile
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            nickname = form.cleaned_data.get('nickname')
            Profile.objects.create(user=user, nickname=nickname)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('pybo:index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
