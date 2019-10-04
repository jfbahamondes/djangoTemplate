from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, label='Nombre')
    last_name = forms.CharField(
        max_length=30, required=False, label='Apellido')
    username = forms.CharField(
        max_length=30, required=True, label='Nombre de Usuario')
    email = forms.EmailField(
        max_length=254, )
    password1 = forms.CharField(
        widget=forms.PasswordInput(), label='Contraseña', )
    password2 = forms.CharField(widget=forms.PasswordInput(
    ), label='Confirmar Contraseña', )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
