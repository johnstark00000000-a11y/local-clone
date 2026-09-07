from django.contrib import admin
from .models import BrainProfile, ChatMessage, UploadItem
admin.site.register(BrainProfile)
admin.site.register(ChatMessage)
admin.site.register(UploadItem)
