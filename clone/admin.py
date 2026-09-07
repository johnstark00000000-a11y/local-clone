from django.contrib import admin
from .models import NeuralClone
@admin.register(NeuralClone)
class NeuralCloneAdmin(admin.ModelAdmin):
    list_display = ("subject_name", "alias", "architecture", "status", "fidelity", "created_at")
