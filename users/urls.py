# urls.py
from django.urls import path
from .views import login_view,dashboard,update_video,custom_logout,usersList,userprofile
from django.contrib.auth.views import LogoutView
urlpatterns = [
    # Other URL patterns
    path('', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('update-video/', update_video, name='update_video'),
    path('users/', usersList, name='userList'),
    path('profile/<int:user_id>/', userprofile, name='profile'),

    path('logout/', custom_logout, name='logout'),

]