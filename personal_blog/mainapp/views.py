from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mainapp.models import PersonalPage


@login_required
def main(request):
    personal_profile = PersonalPage.objects.get(owner=request.user)
    tracking_blogs = PersonalPage.get_news_feed(personal_profile)
    context = {
        'newsfeed': tracking_blogs,
        'self_posts': '',
    }
    return render(request, 'mainapp/index.html', context)
