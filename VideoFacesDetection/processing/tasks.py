from celery import shared_task
from django.http import Http404
from .models import Video
import cv2, face_recognition
import time
import multiprocessing
import threading

CPU_COUNT = multiprocessing.cpu_count()

@shared_task
def start_processing():
    try:
        video = Video.objects.filter( status = "waiting")
    except:
        raise Http404("Видео не найдено")
    print("video", video)
    threads = list()
    for v in video: 
        x = threading.Thread(target=face_detection, args=(v.id,))
        threads.append(x)
        x.start()
        

def face_detection(video_id):
    
    print("video id", video_id)
    try:
        v = Video.objects.get( id = video_id)
    except:
        raise Http404("Видео не найдено")
    if v.status =="completed":
        return
    cap = cv2.VideoCapture(v.video.path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    face_locations = []
    num_faces = 0
    i=0    
    v.update_status(status = "processing")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if v.status == "completed":
            return
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            num_faces += len(face_locations)
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        i +=1
        v.update_progress(i*100/num_frames, num_faces)
    cap.release()
    v.update_status(status = "completed")
