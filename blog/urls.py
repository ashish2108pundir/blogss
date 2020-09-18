
from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.UserRegisterView, name='signup'),



]
