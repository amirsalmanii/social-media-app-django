from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('user_dashboard/<int:user_id>/', views.user_dashboard, name='user_dashboard'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
]