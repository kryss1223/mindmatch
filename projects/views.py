# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProjectForm, AddMembersForm
from .models import Project
from users.models import Skill
from users.models import CustomUser

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.links = {
                'github': form.cleaned_data.get('github'),
                'discord': form.cleaned_data.get('discord'),
            }
            project.save()
            form.save_m2m()  # para skills si es ManyToMany
            print(f"Proyecto guardado: {project.title} por {project.author}")
            # Añadir miembros seleccionados
            member_ids = request.POST.getlist('members')
            for uid in member_ids:
                user = CustomUser.objects.filter(id=uid).first()
                if user:
                    project.members.add(user)

            return redirect('user_profile')  # o donde quieras redirigir
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {
        'form': form,
        'friends': request.user.friends.all()
    })

@login_required
def add_project_members(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = AddMembersForm(request.POST, user=request.user)
        if form.is_valid():
            for member in form.cleaned_data['members']:
                project.members.add(member)
            return redirect('project_detail', project_id=project.id)
    else:
        form = AddMembersForm(user=request.user)

    return render(request, 'projects/add_members.html', {'form': form, 'project': project})

@login_required
def remove_project_member(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id, author=request.user)
    user_to_remove = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        project.members.remove(user_to_remove)
        messages.success(request, f"{user_to_remove.username} eliminado del proyecto.")
        return redirect('project_detail', project_id=project.id)


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id, author=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Idea deleted successfully.")
        return redirect('user_profile')
    return render(request, 'ideas/idea_confirm_delete.html', {'project': project})



@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project, user=request.user)
        if form.is_valid():
            # actualizar info del proyecto
            project = form.save(commit=False)
            project.links = {
                'github': form.cleaned_data.get('github'),
                'discord': form.cleaned_data.get('discord'),
            }
            project.save()
            form.save_m2m()

            # Skills desde input manual
            skills_raw = request.POST.get("skills_input", "")
            skill_names = [s.strip() for s in skills_raw.split(",") if s.strip()]
            project.skills.clear()
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name)
                project.skills.add(skill)

            return redirect('user_profile')
    else:
        form = ProjectForm(instance=project, user=request.user)
        skills_input = ', '.join([s.name for s in project.skills.all()])  # <-- aquí el fix ✅

    return render(request, 'projects/project_form.html', {
        'form': form,
        'project': project,
        'friends': request.user.friends.all(),
        'skills_input': skills_input,
    })
