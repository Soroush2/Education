from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

# assigning the app_name needed for including in urls
app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("profile/<int:user_id>/", views.UserProfileView.as_view(), name="profile"),
    path("buy/<int:post_id>/<int:user_id>/", views.UserBuyView.as_view(), name="buy"),

    # request the reset_password
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'
    ), name='reset_password'),

    # send the reset_password request
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_sent.html'
    ), name='password_reset_done'),

    # confirming the password restoration
    path('reset/<uibd64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # complete the reset_password
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),

]
