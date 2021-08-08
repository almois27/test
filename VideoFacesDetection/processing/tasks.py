from celery import shared_task, task
from celery.result import AsyncResult
from django.http import Http404
from .models import Video
import cv2, face_recognition
# @shared_task
@task(bind=True)
def face_detection(self, video_id):
    print(video_id)
    try:
        v = Video.objects.get( id = video_id)
    except:
        raise Http404("Видео не найдено")
    if v.status in ["completed", "canceled"]:
        return

    self.update_state(state='PROCESSING')    
    v.update_status(status = "processing")


    cap = cv2.VideoCapture(v.video.path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    face_locations = []
    num_faces = 0
    i=0     
    while True:

        while AsyncResult(self.request.id).state == 'PAUSING' or AsyncResult(self.request.id).state == 'PAUSED':
                    if AsyncResult(self.request.id).state == 'PAUSING':
                        print(self.request.id + 'PAUSED')
                        self.update_state(state='PAUSED')
                        v.update_status(status = "paused")     

        if AsyncResult(self.request.id).state == 'RESUME':
                    print(self.request.id + 'RESUMED')
                    self.update_state(state='PROCESSING')
                    v.update_status(status = "processing")
        
        if AsyncResult(self.request.id).state == 'CANCEL':
            print(self.request.id + 'CANCELLED')
            self.update_state(state='CANCELLED')
            v.update_status(status = "canceled")
            return 'CANCELLED'

    
        ret, frame = cap.read()
        if not ret:
            break
        if v.status in ["completed", "canceled"]:
            return
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            num_faces += len(face_locations)
            # for top, right, bottom, left in face_locations:
            #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        i +=1
        v.update_progress(i*100/num_frames, num_faces)
    cap.release()
    v.update_status(status = "completed")
    return 'COMPLETED'