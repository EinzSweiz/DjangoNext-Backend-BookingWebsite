from django.db import models
from useraccounts.models import User

class Inquiry(models.Model):
    class StatusChoice(models.TextChoices):
        OPEN = 'active', 'Active'
        IN_PROGRESS = 'pending', 'Pending'
        CLOSED = 'resolved', 'Resolved'
    class SeverityChoises(models.TextChoices):
        NORMAL = 'normal', 'Normal'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    customer_service = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='customer_service', limit_choices_to=User.RoleChoises.CUSTOMER_SERVICE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=StatusChoice, default=StatusChoice.IN_PROGRESS.value)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    severity = models.CharField(max_length=10, choices=SeverityChoises, default=SeverityChoises.NORMAL.value)
    is_assigned_to_customer_service = models.BooleanField(default=False)

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