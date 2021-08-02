from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('video/',views.upload_video,name='upload'),
    path('video/<int:video_id>/cancel/', views.cancel, name = 'cancel')
]