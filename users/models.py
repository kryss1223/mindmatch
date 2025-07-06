from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser

# Create your models here.
# users/models.py


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=300, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='users')
    
    EXPERIENCE_LEVELS = [
        ('JR', 'Junior'),
        ('MD', 'Mid'),
        ('SR', 'Senior'),
        ('EX', 'Experto'),
    ]

    SPECIALTIES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('fullstack', 'Fullstack'),
        ('designer', 'Designer'),
        ('data', 'Data'),
        ('devops', 'DevOps'),
        # etc.
    ]
    
    STATUS = [
        ('open', 'Open to Work'),
        ('busy', 'Busy'),
        ('living', 'Living Life 😎'),
    ]


    level = models.CharField(max_length=2, choices=EXPERIENCE_LEVELS, blank=True)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES, null=True, blank=True)
    aura = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='open')
    country = CountryField(blank_label='(Select your country)', null=True, blank=True)
    languages = models.ManyToManyField(Language, blank=True, related_name="users")
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    discord = models.URLField(blank=True, null=True)
    
    
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.username


