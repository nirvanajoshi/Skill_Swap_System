from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from .models import Profile, SkillOffered, SkillWanted, SwapRequest, Feedback
from .forms import ProfileForm, SkillOfferedForm, SkillWantedForm, SwapRequestForm, FeedbackForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_edit')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile_edit')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/profile_form.html', {'form': form})


@login_required
def skill_offered_list(request):
    skills = SkillOffered.objects.filter(profile__user=request.user)
    return render(request, 'core/skill_offered_list.html', {'skills': skills})

@login_required
def skill_offered_create(request):
    if request.method == 'POST':
        form = SkillOfferedForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = request.user.profile
            skill.save()
            return redirect('skill_offered_list')
    else:
        form = SkillOfferedForm()
    return render(request, 'core/skill_offered_form.html', {'form': form})

@login_required
def skill_offered_update(request, pk):
    skill = get_object_or_404(SkillOffered, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = SkillOfferedForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skill_offered_list')
    else:
        form = SkillOfferedForm(instance=skill)
    return render(request, 'core/skill_offered_form.html', {'form': form})

@login_required
def skill_offered_delete(request, pk):
    skill = get_object_or_404(SkillOffered, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        skill.delete()
        return redirect('skill_offered_list')
    return render(request, 'core/skill_offered_confirm_delete.html', {'skill': skill})


@login_required
def skill_wanted_list(request):
    skills = SkillWanted.objects.filter(profile__user=request.user)
    return render(request, 'core/skill_wanted_list.html', {'skills': skills})

@login_required
def skill_wanted_create(request):
    if request.method == 'POST':
        form = SkillWantedForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = request.user.profile
            skill.save()
            return redirect('skill_wanted_list')
    else:
        form = SkillWantedForm()
    return render(request, 'core/skill_wanted_form.html', {'form': form})

@login_required
def skill_wanted_update(request, pk):
    skill = get_object_or_404(SkillWanted, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        form = SkillWantedForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('skill_wanted_list')
    else:
        form = SkillWantedForm(instance=skill)
    return render(request, 'core/skill_wanted_form.html', {'form': form})

@login_required
def skill_wanted_delete(request, pk):
    skill = get_object_or_404(SkillWanted, pk=pk, profile__user=request.user)
    if request.method == 'POST':
        skill.delete()
        return redirect('skill_wanted_list')
    return render(request, 'core/skill_wanted_confirm_delete.html', {'skill': skill})


@login_required
def swap_request_list(request):
    swaps = SwapRequest.objects.filter(
        Q(from_profile__user=request.user) | Q(to_profile__user=request.user)
    )
    return render(request, 'core/swap_request_list.html', {'swaps': swaps})

@login_required
def swap_request_create(request):
    if request.method == 'POST':
        form = SwapRequestForm(request.POST)
        if form.is_valid():
            swap = form.save(commit=False)
            swap.from_profile = request.user.profile
            swap.status = 'pending'
            swap.save()
            return redirect('swap_request_list')
    else:
        form = SwapRequestForm()
    return render(request, 'core/swap_request_form.html', {'form': form})

@login_required
def swap_request_accept(request, pk):
    swap = get_object_or_404(SwapRequest, pk=pk, to_profile__user=request.user)
    if request.method == 'POST':
        swap.status = 'accepted'
        swap.save()
        return redirect('swap_request_list')
    return render(request, 'core/swap_request_confirm_accept.html', {'swap': swap})

@login_required
def swap_request_decline(request, pk):
    swap = get_object_or_404(SwapRequest, pk=pk, to_profile__user=request.user)
    if request.method == 'POST':
        swap.status = 'declined'
        swap.save()
        return redirect('swap_request_list')
    return render(request, 'core/swap_request_confirm_decline.html', {'swap': swap})

@login_required
def swap_request_delete(request, pk):
    swap = get_object_or_404(SwapRequest, pk=pk, from_profile__user=request.user)
    if request.method == 'POST':
        swap.delete()
        return redirect('swap_request_list')
    return render(request, 'core/swap_request_confirm_delete.html', {'swap': swap})


@login_required
def feedback_create(request, swap_request_id):
    swap = get_object_or_404(
        SwapRequest, pk=swap_request_id, status='accepted'
    )
    if request.user.profile not in (swap.from_profile, swap.to_profile):
        return redirect('swap_request_list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.from_profile = request.user.profile
            feedback.to_profile = swap.to_profile if request.user.profile == swap.from_profile else swap.from_profile
            feedback.save()
            return redirect('swap_request_list')
    else:
        form = FeedbackForm(initial={'swap_request': swap})
    return render(request, 'core/feedback_form.html', {'form': form, 'swap': swap})