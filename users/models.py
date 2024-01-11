
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20, default='Mr')
    empName = models.CharField(max_length=20, unique=True)
    empID = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    branch = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class VideoUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=50)
    number_of_videos = models.PositiveIntegerField()
    remarks = models.TextField(blank=True)
    upload_datetime = models.DateTimeField(editable=True)

    def __str__(self):
        return f"{self.user.username} - {self.upload_datetime}"
