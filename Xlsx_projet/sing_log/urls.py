from django.urls import path
from . import views
from .views import thanks_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('thanks/', thanks_view, name='thanks'),
]