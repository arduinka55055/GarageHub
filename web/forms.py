from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product, Category


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Your Login', widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget = forms.PasswordInput(attrs={'class':'form-control'}))


class UserRegisterForm(UserCreationForm):
    login = forms.CharField(label='Login name', help_text='Used for authorization on the website', widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Name', help_text='User name must be 150 characters', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('login', 'name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.username = self.cleaned_data["login"] 
        if commit:
            user.save()
        return user


