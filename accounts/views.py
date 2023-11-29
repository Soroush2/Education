from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from home.models import HomeVideo
from home.models import BuyModel


# registering users here
class UserRegisterView(View):
    # if user is already authenticated return them to homepage
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        else:
            return super().dispatch(request, *args, **kwargs)

    # render register form
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "accounts/register.html", {"form": form})

    # save the form if valid
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password1"])
            user = authenticate(request, username=cd["username"], password=cd["password1"])
            if user:
                login(request, user)
            messages.success(request, "You registered successfully!!", "success")
            return redirect("home:home")
        else:
            return render(request, "accounts/register.html", {"form": form})


# login view
class UserLoginView(View):
    # if user is already logged in redirect them to home page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        else:
            return super().dispatch(request, *args, **kwargs)

    # get the login form
    def get(self, request):
        form = UserLoginForm()
        return render(request, "accounts/login.html", {"form": form})

    # save the form if valid
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user:
                login(request, user)
                messages.success(request, "you logged successfully!!", "success")
                return redirect("home:home")
            else:
                messages.error(request, "username or password is wrong!!", "warning")
        else:
            return render(request, "accounts/login.html", {"form": form})


# log out view
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "logout was successful!", "success")
        return redirect("home:home")


# user profile for displaying user information
class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_post = BuyModel.objects.filter(user=user)
        return render(request, "accounts/profile.html", {"user": user, "user_post": user_post})


# view for confirming the purchase of produce
class UserBuyView(LoginRequiredMixin, View):
    def get(self, request, post_id, user_id):
        my_user = User.objects.filter(id=user_id).first()
        homevideo = HomeVideo.objects.filter(id=post_id).first()
        BuyModel(user=my_user, video=homevideo).save()

        messages.success(request, "purchase was successful!", "success")
        return redirect("home:home")
