import random
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import NeuralClone
PIPELINE = ["queued", "scanning", "mapping", "encoding", "stabilizing", "ready"]
def health(request):
    return JsonResponse({"ok": True, "service": "neural-clone"})
def home(request):
    clones = NeuralClone.objects.all()[:8]
    stats = {
        "total": NeuralClone.objects.count(),
        "ready": NeuralClone.objects.filter(status="ready").count(),
        "active": NeuralClone.objects.exclude(status__in=["ready", "failed"]).count(),
    }
    return render(request, "clone/home.html", {"clones": clones, "stats": stats})
def initiate(request):
    if request.method == "POST":
        clone = NeuralClone.objects.create(
            subject_name=request.POST.get("subject_name", "Unknown").strip() or "Unknown",
            alias=request.POST.get("alias", "").strip(),
            architecture=request.POST.get("architecture", "cortical-lattice"),
            fidelity=int(request.POST.get("fidelity") or 87),
            notes=request.POST.get("notes", "").strip(),
            synaptic_density=round(random.uniform(0.12, 0.38), 3),
            coherence=round(random.uniform(0.41, 0.72), 3),
            status="scanning",
        )
        return redirect("clone_detail", pk=clone.pk)
    return render(request, "clone/initiate.html")
def lab(request):
    return render(request, "clone/lab.html", {"clones": NeuralClone.objects.all()})
def clone_detail(request, pk):
    clone = get_object_or_404(NeuralClone, pk=pk)
    return render(request, "clone/detail.html", {"clone": clone, "pipeline": PIPELINE})
@require_POST
def advance(request, pk):
    clone = get_object_or_404(NeuralClone, pk=pk)
    if clone.status in PIPELINE and clone.status != "ready":
        idx = PIPELINE.index(clone.status)
        clone.status = PIPELINE[min(idx + 1, len(PIPELINE) - 1)]
        clone.synaptic_density = min(1.0, clone.synaptic_density + random.uniform(0.08, 0.18))
        clone.coherence = min(0.99, clone.coherence + random.uniform(0.06, 0.14))
        if clone.status == "ready":
            clone.synaptic_density = min(1.0, max(clone.synaptic_density, 0.91))
            clone.coherence = min(0.99, max(clone.coherence, 0.93))
        clone.save()
    return redirect("clone_detail", pk=clone.pk)
def protocol(request):
    return render(request, "clone/protocol.html")
