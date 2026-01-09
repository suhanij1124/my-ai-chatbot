from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)  # Allow empty for images
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)  # New field
    role = models.CharField(max_length=10)  # 'user' or 'ai'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.text or 'Image'}"