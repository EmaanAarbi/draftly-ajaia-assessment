import json
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import Document

class DocumentAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="emaan")
        self.allowed = User.objects.create_user(username="alex")
        self.denied = User.objects.create_user(username="sam")
        self.document = Document.objects.create(owner=self.owner, title="Strategy")
        self.document.shared_with.add(self.allowed)

    def client_as(self, username):
        client = Client()
        session = client.session
        session["demo_user"] = username
        session.save()
        return client

    def test_shared_user_can_save_document(self):
        response = self.client_as("alex").post(
            reverse("documents:save", args=[self.document.pk]),
            data=json.dumps({"title": "Updated strategy", "content": "<p>Shared edit</p>"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, "Updated strategy")

    def test_unshared_user_cannot_open_document(self):
        response = self.client_as("sam").get(reverse("documents:editor", args=[self.document.pk]))
        self.assertEqual(response.status_code, 404)

    def test_blank_title_is_rejected(self):
        response = self.client_as("emaan").post(
            reverse("documents:save", args=[self.document.pk]),
            data=json.dumps({"title": "  ", "content": "<p>Text</p>"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Title is required.")
