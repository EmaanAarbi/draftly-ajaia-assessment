from django.urls import path
from . import views

app_name = "documents"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("users/switch/", views.switch_user, name="switch_user"),
    path("documents/create/", views.create_document, name="create"),
    path("documents/import/", views.import_document, name="import"),
    path("documents/<int:pk>/", views.editor, name="editor"),
    path("documents/<int:pk>/save/", views.save_document, name="save"),
    path("documents/<int:pk>/share/", views.share_document, name="share"),
]
