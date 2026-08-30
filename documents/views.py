import json
from pathlib import Path
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Document

DEMO_USERS = [("emaan", "Emaan Aarbi"), ("alex", "Alex Morgan"), ("sam", "Sam Lee")]

def current_user(request):
    for username, name in DEMO_USERS:
        first, *rest = name.split(" ", 1)
        User.objects.get_or_create(username=username, defaults={"first_name": first, "last_name": rest[0] if rest else ""})
    username = request.session.get("demo_user", "emaan")
    return User.objects.get(username=username)

def accessible_document(pk, user):
    document = get_object_or_404(Document, pk=pk)
    if not document.can_access(user):
        raise Http404("Document not found")
    return document

def dashboard(request):
    user = current_user(request)
    return render(request, "documents/dashboard.html", {
        "current_user": user,
        "users": User.objects.filter(username__in=[u[0] for u in DEMO_USERS]),
        "owned": Document.objects.filter(owner=user),
        "shared": Document.objects.filter(shared_with=user).exclude(owner=user),
    })

@require_POST
def switch_user(request):
    allowed = {u[0] for u in DEMO_USERS}
    username = request.POST.get("username")
    if username in allowed:
        request.session["demo_user"] = username
    return redirect("documents:dashboard")

@require_POST
def create_document(request):
    user = current_user(request)
    document = Document.objects.create(owner=user)
    return redirect("documents:editor", pk=document.pk)

@require_POST
def import_document(request):
    user = current_user(request)
    upload = request.FILES.get("file")
    if not upload:
        messages.error(request, "Choose a .txt or .md file to import.")
        return redirect("documents:dashboard")
    suffix = Path(upload.name).suffix.lower()
    if suffix not in {".txt", ".md"} or upload.size > 1_000_000:
        messages.error(request, "Only .txt and .md files up to 1 MB are supported.")
        return redirect("documents:dashboard")
    try:
        text = upload.read().decode("utf-8")
    except UnicodeDecodeError:
        messages.error(request, "The file must use UTF-8 text encoding.")
        return redirect("documents:dashboard")
    import html
    content = "<p>" + html.escape(text).replace("\n", "</p><p>") + "</p>"
    document = Document.objects.create(owner=user, title=Path(upload.name).stem[:160], content=content)
    return redirect("documents:editor", pk=document.pk)

def editor(request, pk):
    user = current_user(request)
    document = accessible_document(pk, user)
    return render(request, "documents/editor.html", {
        "document": document, "current_user": user,
        "share_candidates": User.objects.exclude(id=user.id),
        "is_owner": document.owner_id == user.id,
    })

@require_POST
def save_document(request, pk):
    user = current_user(request)
    document = accessible_document(pk, user)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request body."}, status=400)
    title = str(payload.get("title", "")).strip()
    content = str(payload.get("content", ""))
    if not title:
        return JsonResponse({"error": "Title is required."}, status=400)
    if len(title) > 160:
        return JsonResponse({"error": "Title must be 160 characters or fewer."}, status=400)
    document.title, document.content = title, content
    document.save(update_fields=["title", "content", "updated_at"])
    return JsonResponse({"ok": True, "updated_at": document.updated_at.isoformat()})

@require_POST
def share_document(request, pk):
    user = current_user(request)
    document = accessible_document(pk, user)
    if document.owner_id != user.id:
        return JsonResponse({"error": "Only the owner can share this document."}, status=403)
    target = get_object_or_404(User, username=request.POST.get("username"))
    if target.id == user.id:
        messages.error(request, "A document is already available to its owner.")
    else:
        document.shared_with.add(target)
        messages.success(request, f"Shared with {target.get_full_name() or target.username}.")
    return redirect("documents:editor", pk=pk)
