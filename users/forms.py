from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.Select, label='Роль')
    seller_name = forms.CharField(max_length=50, required=False, label='Название магазина')
    username = forms.CharField(label='Имя пользователя', help_text='')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text='')

    class Meta:
        model = User
        fields = ('username', 'password')

    def save(self, commit = True):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        role = self.cleaned_data.get('role')
        seller_name = self.cleaned_data.get('seller_name')

        user = User.objects.create_user(
            username = username,
            password = password
        )
        Profile.objects.create(
            user=user,
            role=role,
            seller_name=seller_name
        )

        if commit:
            user.save()

        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
