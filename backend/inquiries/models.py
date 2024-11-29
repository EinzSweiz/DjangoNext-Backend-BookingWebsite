from django.db import models
from useraccounts.models import User

class Inquiry(models.Model):
    class StatusChoice(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        CLOSED = 'closed', 'Closed'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=25, choices=StatusChoice, default=StatusChoice.OPEN.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.subject
    

class Message(models.Model):
    class SenderChoice(models.TextChoices):
        USER = 'user', 'User'
        CUSTOMER_SERVICE = 'customer_service', 'Customer Service'

    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SenderChoice.choices)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.message[:50]}...'