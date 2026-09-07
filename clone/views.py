import random
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import BrainProfile, ChatMessage, UploadItem

def health(request):
    return JsonResponse({"ok": True, "service": "brain2"})

def home(request):
    profiles = BrainProfile.objects.all()[:20]
    return render(request, "clone/home.html", {"profiles": profiles, "total": BrainProfile.objects.count()})

def create_profile(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "User").strip()
        pin = (request.POST.get("pin") or "").strip()
        mood = request.POST.get("mood") or "calm"
        personality = request.POST.get("personality") or "balanced"
        dream = (request.POST.get("dream") or "").strip()
        fear = (request.POST.get("fear") or "").strip()
        hobby = (request.POST.get("hobby") or "").strip()
        about = (request.POST.get("about") or "").strip()
        summary = (
            f"{name} profile. Mood {mood}, personality {personality}. "
            f"Dream: {dream or '—'}. Fear: {fear or '—'}. Hobby: {hobby or '—'}. {about}"
        )
        future = simulate_future(name, personality, dream, fear, hobby, about, [])
        p = BrainProfile.objects.create(
            name=name, pin=pin, mood=mood, personality=personality,
            dream=dream, fear=fear, hobby=hobby, about=about,
            summary=summary, future_note=future,
        )
        request.session["brain_id"] = str(p.id)
        return redirect("dashboard", pk=p.pk)
    return render(request, "clone/create.html")

def dashboard(request, pk):
    p = get_object_or_404(BrainProfile, pk=pk)
    chats = p.messages.order_by("created_at")[:50]
    uploads = p.uploads.order_by("-created_at")[:20]
    return render(request, "clone/dashboard.html", {"p": p, "chats": chats, "uploads": uploads})

def chat(request, pk):
    p = get_object_or_404(BrainProfile, pk=pk)
    if request.method == "POST":
        msg = (request.POST.get("message") or "").strip()
        if msg:
            ChatMessage.objects.create(profile=p, role="user", text=msg)
            reply = reply_from_profile(p, msg)
            ChatMessage.objects.create(profile=p, role="clone", text=reply)
            # refresh future from latest chats
            recent = list(p.messages.order_by("-created_at").values_list("text", flat=True)[:8])
            p.future_note = simulate_future(p.name, p.personality, p.dream, p.fear, p.hobby, p.about, recent)
            p.save(update_fields=["future_note"])
        return redirect("chat", pk=p.pk)
    chats = p.messages.order_by("created_at")
    return render(request, "clone/chat.html", {"p": p, "chats": chats})

def upload_view(request, pk):
    p = get_object_or_404(BrainProfile, pk=pk)
    if request.method == "POST":
        f = request.FILES.get("file")
        note = (request.POST.get("note") or "").strip()
        kind = request.POST.get("kind") or "file"
        title = (request.POST.get("title") or (f.name if f else "log")).strip()
        analysis = analyze_upload(kind, title, note, f)
        item = UploadItem(profile=p, kind=kind, title=title, note=note, analysis=analysis)
        if f:
            item.file = f
        item.save()
        # fold into future
        recent = list(p.messages.order_by("-created_at").values_list("text", flat=True)[:5])
        recent.append(f"upload:{title} {analysis[:80]}")
        p.future_note = simulate_future(p.name, p.personality, p.dream, p.fear, p.hobby, p.about, recent)
        p.save(update_fields=["future_note"])
        return redirect("dashboard", pk=p.pk)
    return render(request, "clone/upload.html", {"p": p})

def future_view(request, pk):
    p = get_object_or_404(BrainProfile, pk=pk)
    if request.method == "POST":
        recent = list(p.messages.order_by("-created_at").values_list("text", flat=True)[:10])
        for u in p.uploads.order_by("-created_at")[:5]:
            recent.append(u.analysis or u.title)
        p.future_note = simulate_future(p.name, p.personality, p.dream, p.fear, p.hobby, p.about, recent)
        p.save(update_fields=["future_note"])
        return redirect("future", pk=p.pk)
    return render(request, "clone/future.html", {"p": p})

def lab(request):
    return render(request, "clone/lab.html", {"profiles": BrainProfile.objects.all()})

def reply_from_profile(p, msg):
    m = msg.lower()
    if any(x in m for x in ["kaun", "who are you"]):
        return f"Main {p.name} ka Brain-2 clone hoon. Teri profile + chat history se respond karta hoon."
    if any(x in m for x in ["sapna", "dream", "future"]):
        return f"Dream side: {p.dream or 'abhi form me clear nahi'}. Future note bhi dashboard pe hai."
    if any(x in m for x in ["dar", "fear", "tension"]):
        return f"Tension zone: {p.fear or 'tune fear field khali chhoda'}."
    if any(x in m for x in ["hobby", "pasand", "video", "upload"]):
        return f"Hobby: {p.hobby or '—'}. Uploads ko main 'memory logs' maanta hoon."
    if any(x in m for x in ["hi", "hello", "hey", "namaste"]):
        return f"Hey {p.name} — bol, aaj kya simulate karein?"
    return (
        f"[{p.personality}/{p.mood}] Samajh gaya: “{msg}”. "
        f"Main history me save karke future guess update karta rehta hoon."
    )

def analyze_upload(kind, title, note, f):
    size = getattr(f, "size", 0) if f else 0
    name = getattr(f, "name", title) if f else title
    if kind == "video":
        return (
            f"Video log '{name}' receive hua (\~{size} bytes). "
            f"Demo analysis: motion/emotion tags simulated. Note: {note or '—'}. "
            f"Is memory ko clone timeline me add kiya."
        )
    if kind == "image":
        return f"Image '{name}' stored as visual memory. Note: {note or '—'}."
    if kind == "log":
        return f"Text/activity log saved. {note or name}"
    return f"File '{name}' attached as brain memory fragment. {note or ''}"

def simulate_future(name, personality, dream, fear, hobby, about, recent):
    recent_txt = " | ".join([str(x)[:60] for x in recent[:6]]) if recent else "no chats yet"
    paths = [
        f"Agar {name} {hobby or 'apni routine'} pe consistent raha, 1 saal me {dream or 'apna goal'} ke kareeb ho sakta hai.",
        f"Risk side: {fear or 'unknown fears'} ignore hue to progress slow ho sakta hai.",
        f"Personality ({personality}) ke hisaab se best path: chhote daily experiments + weekly review.",
        f"Recent signals: {recent_txt}.",
        f"Brain-2 suggestion: har upload/chat ko memory maan kar next 30 din ka simple plan banao.",
    ]
    if about:
        paths.append(f"Self-note influence: {about[:120]}")
    return " ".join(paths)
