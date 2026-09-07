import uuid, django.utils.timezone
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="BrainProfile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=80)),
                ("pin", models.CharField(blank=True, max_length=20)),
                ("mood", models.CharField(default="calm", max_length=40)),
                ("personality", models.CharField(default="balanced", max_length=40)),
                ("dream", models.CharField(blank=True, max_length=200)),
                ("fear", models.CharField(blank=True, max_length=200)),
                ("hobby", models.CharField(blank=True, max_length=120)),
                ("about", models.TextField(blank=True)),
                ("summary", models.TextField(blank=True)),
                ("future_note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="UploadItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(default="file", max_length=20)),
                ("title", models.CharField(blank=True, max_length=120)),
                ("file", models.FileField(blank=True, null=True, upload_to="brain_uploads/%Y/%m/")),
                ("note", models.TextField(blank=True)),
                ("analysis", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="uploads", to="clone.brainprofile")),
            ],
        ),
        migrations.CreateModel(
            name="ChatMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(max_length=10)),
                ("text", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="clone.brainprofile")),
            ],
        ),
    ]
