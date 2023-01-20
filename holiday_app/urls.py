
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("api/holidays/", views.HolidayView.as_view(), name="holiday_create"),
    path("api/create-user/", views.CreateUserView.as_view(), name="create_user"),
    path("api/login/", views.LoginUserView.as_view(), name="login_user"),
    path("api/logout/", views.LogoutUserView.as_view(), name="logout_user"),
]
