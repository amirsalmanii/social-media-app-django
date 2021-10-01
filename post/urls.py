from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('post/<slug:slug>/<int:id>/', views.detail_post, name='detail_post'),
    path('add_post/<int:user_id>/', views.add_post, name='add_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:post_id>/<int:post_user_id>', views.edit_post, name='edit_post'),
    path('reply/<int:comment_id>/<int:post_id>/', views.add_reply, name='add_reply'),
]