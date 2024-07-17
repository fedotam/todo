from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    # Choices for the priority field
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    # ForeignKey relationship to associate each task with a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Title of the task with a max length of 200 characters
    title = models.CharField(max_length=200)
    # Description of the task, can be null or blank
    description = models.TextField(null=True, blank=True)
    # Boolean field to mark whether the task is complete or not
    complete = models.BooleanField(default=False)
    # Timestamp when the task is created, auto-populated on creation
    created = models.DateTimeField(auto_now_add=True)
    # Due date for the task, default is the current date
    due_date = models.DateField(default=timezone.now)
    # Priority of the task, with choices of 'Low', 'Medium', and 'High', default is 'Medium'
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')

    # String representation of the task object, returns the title of the task
    def __str__(self):
        return self.title

    # Meta class to define model-specific options
    class Meta:
        # Order tasks by the 'complete' field (False first, then True)
        ordering = ['complete']
