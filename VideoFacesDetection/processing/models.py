from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/")

    status = models.CharField(max_length=100, default = "waiting")
    num_faces = models.IntegerField(default = 0)
    task_id = models.CharField(max_length=200, default = "")
    progress = models.PositiveSmallIntegerField(
        default=0,
        editable=False
    )

    def __str__(self):
        return '{} {} ({:d}% {})'.format(self.title, self.status,
                                    self.progress, self.num_faces)

    def update_progress(self, percent, num_faces, commit=True):
        if 0 > percent > 100:
            raise ValueError("Invalid percent value.")

        self.progress = percent
        self.num_faces = num_faces
        if commit:
            self.save()

    def update_status(self, status="canceled" , commit=True):
        self.status = status
        if commit:
            self.save()

    def update_task_id(self, task_id, commit=True):
        self.task_id = task_id
        if commit:
            self.save()