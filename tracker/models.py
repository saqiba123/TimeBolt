from django.db import models

# Create your models here.
class TrackerModel(models.Model):
    task_name = models.CharField(max_length=30)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True,blank=True)
    duration = models.DurationField(null=True,blank=True)
    
    def __str__(self):
        return self.task_name