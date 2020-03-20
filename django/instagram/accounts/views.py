from django.contrib import messages
from django.http.response import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    Http404,
    HttpResponseBadRequest,
)
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView
from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout

from .forms import SignUpForm, UserLoginForm


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy("photo:index")

    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()  # Sets a test cookie to make sure the user has cookies enabled

        if request.user.is_authenticated:
            return redirect("photo:index")
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.get_username(), password=form.get_password())
        if user is not None:
            login(self.request, user)

        return super(UserLoginView, self).form_valid(form)


class SignUpView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("photo:index")
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/signup.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        try:
            form.signup()
        except forms.ValidationError as e:
            messages.warning(request, str(e))
            return redirect("/")
        return redirect("photo:index")

