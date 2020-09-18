
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.PostListView.as_view(),name='post_list'),
    path('about/',views.AboutView.as_view(),name='about'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/edit/<int:pk>/', views.PostDeleteView.as_view(), name='post_edit'),
    path('post/draft/', views.DraftListView.as_view(), name='draft'),
    path('post/remove/<int:pk>/', views.PostDeleteView.as_view(), name='post_remove'),
    path('post/<int:pk>/publish', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('accounts/login/',views.Login, name='login'),
    


]



