from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Skill
from ideas.models import Idea
from projects.models import Project
from django.db.models import Count, Q


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logea al usuario automáticamente
            return redirect('home')  # Cambia por tu vista de usuario
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Cambia 'profile' por la url que quieras
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def home(request):
    # Aquí puedes pasar datos reales luego, por ahora vacío
    return render(request, 'users/home.html')

@login_required
def user_settings(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            skills_input = request.POST.get('skills_input', '')
            skill_names = [s.strip() for s in skills_input.split(',') if s.strip()]

            current_skills = set(request.user.skills.values_list('name', flat=True))
            for name in skill_names:
                if name not in current_skills:
                    skill_obj, _ = Skill.objects.get_or_create(name=name)
                    user.skills.add(skill_obj)

            user.save()
            return redirect('user_profile', username=request.user.username)
    else:
        # Este bloque se ejecuta en GET
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/settings.html', {
        'form': form,
    })



@login_required
def user_profile(request):
    # Simple: pasamos el usuario logueado al template
    return render(request, 'users/profile.html', {'user': request.user})



@login_required
def home(request):
    ideas = Idea.objects.filter(
        status='open',
        privacy='public'
    )

    projects = Project.objects.filter(privacy='public')  # añade esto
    query = request.GET.get('q')
    if query :
        ideas = ideas.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__username__icontains=query) |
            Q(skills_required__name__icontains=query)
        )   

    # Filtrar usuarios por nombre de usuario o skills si quieres
        users = User.objects.filter(
            Q(username__icontains=query)
        ).distinct()
    else:
        users = User.objects.all()

    # Filtro por skills si hay input
    skills_input = request.GET.get('skills')
    if skills_input:
        skill_names = [s.strip() for s in skills_input.split(',') if s.strip()]
        for name in skill_names:
            ideas = ideas.filter(skills_required__name__iexact=name)

    # Ordenamos por likes y luego por fecha
    ideas = ideas.annotate(
        num_likes=Count('likes')
    ).order_by('-num_likes', '-created_at')[:10]

    
    return render(request, 'users/home.html', {
        'ideas': ideas,
        'users':users,
        'projects': projects,
    })



def user_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    projects = Project.objects.filter(author=user)
    return render(request, 'users/profile.html', {'user': user, 'projects': projects})

@login_required
def my_profile(request):
    user = request.user
    projects = Project.objects.filter(author=user)
    return render(request, 'users/profile.html', {'user': user, 'projects': projects})


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        request.user.friends.add(target_user)
    return redirect('user_profile_view', username=username)

@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        request.user.friends.remove(target_user)
    return redirect('user_profile_view', username=username)

@login_required
def user_friends(request, username):
    user = get_object_or_404(User, username=username)
    friends = user.friends.all()
    
    query = request.GET.get('q')
    if query:
        friends = friends.filter(username__icontains=query)

    return render(request, 'users/user_friends.html', {
        'user_profile': user,
        'friends': friends,
        'query': query,
    })
