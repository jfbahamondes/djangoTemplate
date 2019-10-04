from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from session.forms import SignUpForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'session/signup.html', {'form': form})


def loginUser(request):

    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }


    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Usuario o contraseña incorrecta")
            return render(request, "session/login.html", context)

        messages.success(request, "Bienvenido!")
        login(request, user)
        return redirect("index")
    return render(request, "session/login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Adios!")
    return redirect("index")
