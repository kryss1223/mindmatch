# Create your models here.
from django.db import models
from django.conf import settings


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
    ]
    ACTIVE_STATE_CHOICES = [
        ('review', 'Reviewing'),
        ('searching', 'Hiring'),
        ('development', 'Only develop'),
    ]
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends', 'Only Friends'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects_authored')
    published_at = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField('users.Skill', blank=True)  
    availability = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    active_state = models.CharField(max_length=20, choices=ACTIVE_STATE_CHOICES, blank=True, null=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects_joined', blank=True)
    links = models.JSONField(blank=True, null=True)  # Para guardar links como github, discord, etc. Ej: {"github":"url", "discord":"url"}

    def save(self, *args, **kwargs):
        # Si no está activa, no tiene active_state
        if self.availability != 'active':
            self.active_state = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
