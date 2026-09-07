import uuid
from django.db import models
from django.utils import timezone
class NeuralClone(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"), ("scanning", "Cortical Scan"), ("mapping", "Connectome Mapping"),
        ("encoding", "Synaptic Encoding"), ("stabilizing", "Pattern Stabilization"),
        ("ready", "Clone Ready"), ("failed", "Failed"),
    ]
    ARCHITECTURE = [
        ("cortical-lattice", "Cortical Lattice v4"), ("hippocampal-mesh", "Hippocampal Mesh"),
        ("thalamic-relay", "Thalamic Relay Grid"), ("full-connectome", "Full Connectome Mirror"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject_name = models.CharField(max_length=120)
    alias = models.CharField(max_length=80, blank=True)
    architecture = models.CharField(max_length=40, choices=ARCHITECTURE, default="cortical-lattice")
    fidelity = models.PositiveSmallIntegerField(default=87)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="queued")
    notes = models.TextField(blank=True)
    synaptic_density = models.FloatField(default=0.0)
    coherence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.subject_name} ({self.get_status_display()})"
    def display_alias(self):
        return self.alias or f"NCP-{str(self.id)[:8].upper()}"
