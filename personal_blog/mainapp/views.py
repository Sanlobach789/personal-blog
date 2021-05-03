from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.models import User
from mainapp.forms import PostCreationForm
from mainapp.models import PersonalPage, PostItem


@login_required
def main(request):
    personal_profile = PersonalPage.objects.get(owner=request.user)
    self_posts = personal_profile.get_self_posts()
    context = {
        'self_posts': self_posts,
    }
    return render(request, 'mainapp/index.html', context)


def news_feed(request):
    personal_profile = PersonalPage.objects.get(owner=request.user)
    tracking_blogs = personal_profile.get_news_feed()
    context = {
        'newsfeed': tracking_blogs,
    }
    return render(request, 'mainapp/news_feed.html', context)


def users_list(request):
    personal_profile = PersonalPage.objects.get(owner=request.user)
    blogs = personal_profile.show_users()
    context = {
        'untracked_users': blogs['untracked_users'],
        'tracking_users': blogs['tracking_users'],
    }
    return render(request, 'mainapp/blogs_list.html', context)


def subscribe(request, user_id):
    personal_profile = PersonalPage.objects.get(owner=request.user)
    user = User.objects.get(id=user_id)
    personal_profile.tracking_blogs.add(user)
    return HttpResponseRedirect(reverse('mainapp:blogs'))


def unsubscribe(request, user_id):
    personal_profile = PersonalPage.objects.get(owner=request.user)
    user = User.objects.get(id=user_id)
    personal_profile.tracking_blogs.remove(user)
    return HttpResponseRedirect(reverse('mainapp:blogs'))


def create_new_post(request):
    if request.method == 'POST':
        personal_profile = PersonalPage.objects.get(owner=request.user)
        form = PostCreationForm(data=request.POST)
        if form.is_valid():
            title = request.POST['title']
            content = request.POST['content']
            PostItem.objects.create(title=title, content=content, blog=personal_profile)
    else:
        form = PostCreationForm()
    context = {'form': form}
    return render(request, 'mainapp/create_post.html', context)


def delete_post(request, post_id):
    PostItem.objects.get(id=post_id).delete()
    return HttpResponseRedirect(reverse('mainapp:index'))
