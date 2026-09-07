import uuid
from django.db import models
from django.utils import timezone

class BrainProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80)
    pin = models.CharField(max_length=20, blank=True)  # simple access code
    mood = models.CharField(max_length=40, default="calm")
    personality = models.CharField(max_length=40, default="balanced")
    dream = models.CharField(max_length=200, blank=True)
    fear = models.CharField(max_length=200, blank=True)
    hobby = models.CharField(max_length=120, blank=True)
    about = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    future_note = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    profile = models.ForeignKey(BrainProfile, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10)  # user | clone
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

class UploadItem(models.Model):
    profile = models.ForeignKey(BrainProfile, on_delete=models.CASCADE, related_name="uploads")
    kind = models.CharField(max_length=20, default="file")  # file | video | image | log
    title = models.CharField(max_length=120, blank=True)
    file = models.FileField(upload_to="brain_uploads/%Y/%m/", blank=True, null=True)
    note = models.TextField(blank=True)
    analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
