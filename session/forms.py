from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    passwordAttrs = {
        "type": "password",
        "autocomplete": "new-password",
    }
    textAttrs = {
        "type": "text",
        "autocomplete": "on",
    }
    emailAttrs = {
        "type": "email",
        "autocomplete": "on",
    }
    first_name = forms.CharField(
        max_length=30, required=False, label='Nombre',
        widget=forms.TextInput(attrs=textAttrs))
    last_name = forms.CharField(
        max_length=30, required=False, label='Apellido',
        widget=forms.TextInput(attrs=textAttrs))
    username = forms.CharField(
        max_length=30, required=True, label='Nombre de Usuario',
        widget=forms.TextInput(attrs=textAttrs))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs=emailAttrs),
        max_length=254, )
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs=passwordAttrs), label='Contraseña', )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs=passwordAttrs), label='Confirmar Contraseña', )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
