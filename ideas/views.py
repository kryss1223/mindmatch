# ideas/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import IdeaForm, CommentForm
from django.shortcuts import get_object_or_404, render
from .models import Idea, Comment

from users.models import Skill



@login_required
def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.method == 'POST':
        if 'like' in request.POST:
            if request.user in idea.likes.all():
                idea.likes.remove(request.user)
            else:
                idea.likes.add(request.user)
            return redirect('idea_detail', idea_id=idea.id)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.idea = idea
                comment.save()
                return redirect('idea_detail', idea_id=idea.id)
    else:
        form = CommentForm()

    return render(request, 'ideas/idea_detail.html', {
        'idea': idea,
        'comment_form': form,
        'has_liked': request.user in idea.likes.all()
    })

@login_required
def create_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        skills_input = request.POST.get('skills_input', '')
        skill_names = [s.strip() for s in skills_input.split(',') if s.strip()]
        
        if form.is_valid():
            idea = form.save(commit=False)
            idea.author = request.user
            idea.save()

            # Procesar skills
            idea.skills_required.clear()
            for name in skill_names:
                skill_obj, _ = Skill.objects.get_or_create(name=name)
                idea.skills_required.add(skill_obj)

            return redirect('idea_detail', idea_id=idea.id)
    else:
        form = IdeaForm()

    return render(request, 'ideas/create_idea.html', {'form': form, 'skills_input': ''})


@login_required
def idea_delete(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, author=request.user)
    if request.method == "POST":
        idea.delete()
        messages.success(request, "Idea deleted successfully.")
        return redirect('user_profile')
    return render(request, 'ideas/idea_confirm_delete.html', {'idea': idea})
