from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserForm(UserCreationForm):
    nickname = forms.CharField(label='닉네임', max_length=30)
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password1', 'password2')

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('이미 사용 중인 닉네임입니다.')
        return nickname
