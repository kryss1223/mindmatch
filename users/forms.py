# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Skill, Languaje
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Existing email.")
        return email
    


EXPERIENCE_LEVELS = [
    ('JR', 'Junior'),
    ('MD', 'Mid'),
    ('SR', 'Senior'),
    ('EX', 'Experto'),
]

STATUS = [
    ('open', 'Open to Work'),
    ('busy', 'Busy'),
    ('living', 'Living Life 😎'),
]

SPECIALTIES = [
    ('backend', 'Backend'),
    ('frontend', 'Frontend'),
    ('fullstack', 'Fullstack'),
    ('designer', 'Designer'),
    ('data', 'Data'),
    ('devops', 'DevOps'),
]

class CustomUserChangeForm(UserChangeForm):
    password = None
    username = forms.CharField(disabled=True)

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white',
            'size': '6'
        }),
        required=False
    )

    level = forms.ChoiceField(
        choices=EXPERIENCE_LEVELS,
        widget=forms.RadioSelect,
        required=False
    )

    specialty = forms.ChoiceField(
        choices=SPECIALTIES,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
        required=False
    )

    status = forms.ChoiceField(
        choices=STATUS,
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
        required=False
    )

    country = forms.CharField(
        required=False,
        widget=CountrySelectWidget(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'})
    )

    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'text-white'}),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'bio', 'level', 'specialty', 'status', 'country',
            'languages', 'github', 'linkedin', 'twitter', 'discord', 'skills'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')