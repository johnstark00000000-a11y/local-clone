import uuid
import django.utils.timezone
from django.db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="NeuralClone",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("subject_name", models.CharField(max_length=120)),
                ("alias", models.CharField(blank=True, max_length=80)),
                ("architecture", models.CharField(choices=[("cortical-lattice", "Cortical Lattice v4"), ("hippocampal-mesh", "Hippocampal Mesh"), ("thalamic-relay", "Thalamic Relay Grid"), ("full-connectome", "Full Connectome Mirror")], default="cortical-lattice", max_length=40)),
                ("fidelity", models.PositiveSmallIntegerField(default=87)),
                ("status", models.CharField(choices=[("queued", "Queued"), ("scanning", "Cortical Scan"), ("mapping", "Connectome Mapping"), ("encoding", "Synaptic Encoding"), ("stabilizing", "Pattern Stabilization"), ("ready", "Clone Ready"), ("failed", "Failed")], default="queued", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("synaptic_density", models.FloatField(default=0.0)),
                ("coherence", models.FloatField(default=0.0)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
