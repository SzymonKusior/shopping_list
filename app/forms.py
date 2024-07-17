# from django import forms
from django.forms import ModelForm,TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        widgets = {
            "username": TextInput(attrs={"help_text": None, "class": "username_field", "id":"usernameLoginField"}), 
            "password": PasswordInput(),
        }

    # username = forms.CharField(help_text=None, widget=TextInput(attrs={"class":'username_field'}))

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]