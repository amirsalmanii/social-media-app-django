from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

from .forms import LoginForm, RegisterForm, EditProfile
from .models import Profile, Relation
from post.models import Post

def login_user(request):
    if request.user.is_authenticated:
        return redirect('post:all_posts')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(password=cd['password'], username=cd['username'])
            if user is not None:
                login(request, user)
                messages.success(request, 'user login successfully')
                return redirect('post:all_posts')
            else:
                messages.error(request, 'user dosent exist')
                return redirect('account:login_user')
    else:
        form = LoginForm()
    return render(request, 'account/account_app_forms.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, 'account created successfully', extra_tags='success')
            return redirect('post:all_posts')
    else:
        form = RegisterForm()
    return render(request, 'account/account_app_forms.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'logout successfully', extra_tags='success')
    return redirect('post:all_posts')


@login_required
def user_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=user)
    rel = Relation.objects.filter(from_user=request.user, to_user=user)
    have_rel = False
    if rel:
        have_rel = True
    return render(request, 'account/user_dahboard.html', {'user': user, 'posts': posts, 'rel': have_rel,})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=profile)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            user.username = cd['username']
            user.email = cd['email']
            user.save()
            messages.success(request, 'update profile successfully')
            return redirect('account:user_dashboard', user_id)
    else:
        form = EditProfile(instance=profile, initial={'email': user.email, 'username': user.username})
    return render(request, 'account/account_app_forms.html', {'form': form})


def follow(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id') #get data from jquer_ajax
        user = get_object_or_404(User, id=user_id)
        Relation(from_user=request.user, to_user=user).save()
        return JsonResponse({'status': 'ok'})



def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id') #get data from jquer_ajax
        user = get_object_or_404(User, id=user_id)
        rel = get_object_or_404(Relation, from_user=request.user, to_user=user)
        rel.delete()
        return JsonResponse({'status': 'ok'})