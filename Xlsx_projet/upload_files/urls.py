# upload_files/urls.py
from django.urls import path
from . import views
from .views import check_data

app_name = 'upload_files'

urlpatterns = [
    path('upload_file/', views.upload_file, name='upload_file'),
    path('check_data/', check_data, name='check_data'),
]