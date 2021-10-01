from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from .models import Post, Comment
from .forms import Add_EditPostForm, Add_Commen_Add_Reply_Form

def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'post/all_posts.html', {'posts': posts})


def detail_post(request, slug, id):
    post = get_object_or_404(Post, slug=slug, id=id)
    comments = post.pcomment.all() # == Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = Add_Commen_Add_Reply_Form(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Comment successfully sent')
            return redirect('post:detail_post', slug, id)
    else:
        form = Add_Commen_Add_Reply_Form()
    context = {
    'post': post,
    'comments': comments,
    'form': form,
    }
    return render(request, 'post/detail_post.html', context)


@login_required
def add_post(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = Add_EditPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = user
            new_post.slug = slugify(form.cleaned_data['body'][:20])
            new_post.save()
            return redirect('account:user_dashboard', user_id)
    else:
        form = Add_EditPostForm()
    return render(request, 'post/post_app_forms.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user_id = post.user.id  #for return to user dashboard
    post.delete()
    return redirect('account:user_dashboard', user_id)


@login_required
def edit_post(request, post_id, post_user_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, id=post_user_id) #for set user
    if request.method == 'POST':
        form = Add_EditPostForm(request.POST, instance=post)
        if form.is_valid():
            edit_post = form.save(commit=False)
            edit_post.user = user
            edit_post.slug = slugify(form.cleaned_data['body'][:20])
            edit_post.save()
            return redirect('account:user_dashboard', post_user_id)
    else:
        form = Add_EditPostForm(instance=post)
    return render(request, 'post/post_app_forms.html', {'form': form})


def add_reply(request, comment_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, reply='False')
    if request.method == 'POST':
        form = Add_Commen_Add_Reply_Form(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'reply successfuly sended')
            return redirect('post:detail_post', post.slug, post_id)
    else:
        return redirect('post:all_post')