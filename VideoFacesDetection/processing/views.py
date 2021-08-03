from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Video
import cv2, face_recognition
from django.db import transaction

from celery.result import AsyncResult
from .tasks import start_processing

import multiprocessing
import threading

CPU_COUNT = multiprocessing.cpu_count()


def index(request):
    pass

def upload_video(request):
   
    if request.method == 'POST':
        #Загрузка видео на обработку.
        files = request.FILES.getlist('video')
        
        for f in files:
            print("file", f)
            content = Video(title=f,video=f, status = "waiting", num_faces = 0)
            content.save()  
        transaction.on_commit(lambda: start_processing.delay())   
        return HttpResponseRedirect(reverse('upload'))

    elif request.method == 'GET':
        #Получение текущего статуса (включая агрегацию результатов процессинга) по всем загруженным видео.
        v = Video.objects.all()  
        #transaction.on_commit(lambda: start_processing.delay())  
        return render(request,'upload.html', {'video_list':v})



def cancel(request, video_id):
      #Отмена/остановка обработки для выбранного видео.
    try:
        v = Video.objects.get( id = video_id)
    except:
        raise Http404("Видео не найдено")
    return render(request,'videos.html',{'video':v})


