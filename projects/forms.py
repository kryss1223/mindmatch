from django import forms
from .models import Project
from users.models import Skill, CustomUser

class ProjectForm(forms.ModelForm):
    github = forms.CharField(required=False)
    discord = forms.CharField(required=False)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white',
            'size': '6'
        }),
        required=False
    )

    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.none(),  # se actualiza en __init__
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white',
            'size': '6'
        }),
        required=False
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'skills', 'availability', 'privacy', 'links', 'active_state', 'members']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
            'availability': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
            'privacy': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
            'active_state': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
            'links': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # te paso el user desde la view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['members'].queryset = user.friends.all()

        if self.instance and self.instance.pk and self.instance.links:
            self.fields['github'].initial = self.instance.links.get('github', '')
            self.fields['discord'].initial = self.instance.links.get('discord', '')
            self.fields['members'].initial = self.instance.members.all()


class AddMembersForm(forms.Form):
    members = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={
            'class': 'w-full px-4 py-2 rounded bg-[#1C114A] text-white',
            'size': '6'
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Pasas el usuario desde la view
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = user.friends.all()
