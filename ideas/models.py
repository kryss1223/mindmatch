from django.db import models
from django.conf import settings
# Create your models here.

class Idea(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('friends', 'Friends Only'),
        ('private', 'Private'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('epic', 'Epic'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='open')
    privacy = models.CharField(max_length=7, choices=PRIVACY_CHOICES, default='public')
    skills_required = models.ManyToManyField('users.Skill', blank=True, related_name='ideas')
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_LEVELS, blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_ideas', blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_ideas', blank=True)


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'Comment by {self.author.username} on {self.idea.title}'
