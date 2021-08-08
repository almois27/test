from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('video/',views.upload_video,name='upload'),
    path('video/<int:video_id>/cancel/', views.cancel, name = 'cancel'),
    path('video/<int:video_id>/cancel/get_task_id', views.get_task_id, name = 'cancel_get_task_id'),
    path('video/<int:video_id>/cancel/get_task_info', views.get_task_info_cancel, name = 'get_task_info_cancel'),
    path('video/get_task_info/', views.get_task_info, name = 'get_task_info'),
    path('video/get_task_list/', views.get_task_list, name = 'get_task_list')
]