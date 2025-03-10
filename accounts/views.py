from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            print('é post')
            form = RegistrationForm(request.POST or None)
            print(request.POST)
            print(form)
            # checa se é valido
            if form.is_valid():
                user = form.save()

                raw_password = form.cleaned_data.get('password1')

                print(raw_password)
                user = authenticate(
                    username=user.username,
                    password=raw_password
                )
                login(request, user)

                return redirect("main:home")
        else:
            form = RegistrationForm()

        return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:home")
    else:
        if request.method == "POST":
            print('eh post')
            print(request.POST)
            username = request.POST['username']
            password = request.POST['password']

            # checa as credenciais
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("main:home")
                else:
                    return render(request, 'accounts/login.html', {"error": "Sua conta foi desabilitada!"})
            else:
                return render(request, 'accounts/login.html', {"error": "Usuário ou senha incorretos. Tente novamente"})
        return render(request, 'accounts/login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("main:home")
    else:
        return redirect("main:home")
