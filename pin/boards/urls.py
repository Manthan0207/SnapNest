from django.shortcuts import render

# Create your views here.
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="Home") ,
    path('profile/',views.profile,name="Profile") ,
    path('signup/',views.handleSignUp,name="HandleSignUp"),
    path('login/',views.handleLogin,name="HandleLogin"),
    path('logout/',views.handleLogOut,name="HandleLogOut"),
    path('aboutus/',views.aboutus,name="About"),
    path('pin/<int:image_id>/', views.pin, name='pin-view'),
    path('upload_pin',views.upload_pin,name="upload_pin"),
    path('upload_img',views.upload_img,name="upload_img"),
    path('user/<str:username>/', views.user_profile, name='user-profile'),
    path('toggle-like/<int:image_id>/', views.toggle_like, name='toggle-like'),
    path('search/',views.search_page,name='search-page'),
    path('toggle-follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    path('login-page', views.login_page, name='login-page'),
    path('signupPage', views.signup_page, name='signupPage'),
    path('save/<int:image_id>/',views.save,name='save'),
    path('analytics/<int:image_id>/',views.analytics,name='analytics'),
    path('notifications/', views.notifications, name='notifications'),
    path('delete-pin/<int:image_id>', views.delete_pin, name='delete-pin'),
    path("report-pin/<int:image_id>/", views.report_pin, name="report-pin"),
   


]
