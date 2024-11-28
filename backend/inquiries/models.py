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