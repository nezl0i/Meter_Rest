from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib import messages


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, 'Некорректные данные')
                # msg = 'Некорректные данные'
        else:
            # msg = 'Ошибка в веденных данных'
            messages.error(request, 'Ошибка в веденных данных')
    context = {
        'title': 'Вход',
        'msg': msg,
        'form': form
    }

    return render(request, "authentication/login.html", context)


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            messages.info(request, 'Пользователь создан успешно')
            msg = '<a href="/login/">Вход</a>'
            success = True
            return redirect("/login/")
        else:
            # msg = 'Форма заполнена неправильно'
            messages.error(request, 'Проверьте правильность введенных данных')
    else:
        form = SignUpForm()
    context = {
        'title': 'Регистрация',
        'msg': msg,
        'form': form,
        'success': success
    }

    return render(request, "authentication/register.html", context)
