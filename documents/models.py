from django.contrib.auth.models import User
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=160, default="Untitled document")
    content = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_documents")
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_documents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def can_access(self, user):
        return self.owner_id == user.id or self.shared_with.filter(id=user.id).exists()
