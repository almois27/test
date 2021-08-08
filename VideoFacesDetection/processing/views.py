from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db import transaction
import json
import multiprocessing
from celery.result import AsyncResult
from VideoFacesDetection.celery import app
from .tasks import face_detection
from .models import Video
from celery.app.task import Task

CPU_COUNT = multiprocessing.cpu_count()
INSPECT_CELERY = app.control.inspect()  

TASKS = {}
def start_processing():
    global INSPECT_CELERY
    try:
        num_tasks = len(list(INSPECT_CELERY.active().values())[0])
    except:
        return
    try:
        video = Video.objects.filter( status = "waiting")
    except:
        raise Http404("Видео не найдено")
    
    for v in video:
        if num_tasks>=CPU_COUNT:
            return
        t = face_detection.delay(v.id)
        v.update_task_id(t.task_id)
    

def index(request):
    pass

def get_task_info(request):
    v_id = request.GET.get('v_id', None)
    try:
        v = Video.objects.get( id = v_id)
    except:
        raise Http404("Видео не найдено")
    data =  {
        "status" : v.status,
        "progress" : v.progress,
        "result" : v.num_faces,
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
    
def get_task_list(request):
    v = Video.objects.all()
    data = {
        "video_list" : list(v.values()),
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
    

def upload_video(request):
   
    if request.method == 'POST':
        #Загрузка видео на обработку.
        files = request.FILES.getlist('video')
        
        for f in files:
            print("file", f)
            content = Video(title=f,video=f, status = "waiting", num_faces = 0, task_id="")
            content.save()  
        #transaction.on_commit(lambda: start_processing.delay())   
        return HttpResponseRedirect(reverse('upload'))

    elif request.method == 'GET':
        #Получение текущего статуса (включая агрегацию результатов процессинга) по всем загруженным видео.
               
        v = Video.objects.all()  
        start_processing()
        data = {
            "video_list" : list(v.values())
        }
        
        return render(request,'upload.html', data)



def cancel(request, video_id):

    #Отмена/остановка обработки для выбранного видео.
    try:
        v = Video.objects.get( id = video_id)
    except:
        raise Http404("Видео не найдено")
    
    if request.GET.get('stop_click'):
        t_id = v.task_id
        cancel_task(t_id)
        # task_res = AsyncResult(t_id)
        # if task_res.ready():
        #     return render(request,'video.html',{'video':v}) 
        # app.control.revoke(t_id, terminate = True)
        # v.update_status("canceled")
    if request.GET.get('pause_click'):        
        t_id = v.task_id
        pause_task(t_id)
    if request.GET.get('resume_click'):
        t_id = v.task_id
        resume_task(t_id)
    return render(request,'video.html',{'video':v})
    
def get_task_id(request, video_id):
    return HttpResponse(json.dumps({'video_id':video_id}), content_type='application/json')

def get_task_info_cancel(request, video_id):
    return get_task_info(request)    
    
def pause_task(tid):
    Task.update_state(self=face_detection, task_id=tid, state='PAUSING')
    return 'Your task will be paused !'


def resume_task(tid):
    Task.update_state(self=face_detection, task_id=tid, state='RESUME')
    return 'Your task will be resumed !'


def cancel_task(tid):
    Task.update_state(self=face_detection, task_id=tid, state='CANCEL')
    return 'Your task will be cancelled !'

