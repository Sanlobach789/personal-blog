from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import User
from django.db import models, transaction


class PersonalPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tracking_blogs = models.ManyToManyField(User, related_name='followed_blogs')

    def __str__(self):
        return f'{self.name}'

    def get_self_posts(self):
        posts = PostItem.objects.filter(blog=self.id)
        return posts

    def get_news_feed(self):
        posts = PostItem.objects.filter(blog__owner__in=self.tracking_blogs.values('id')).order_by('-created')
        viewed_posts_id = ViewedPosts.get_viewed_posts(self.owner)
        new_posts = posts.exclude(id__in=viewed_posts_id)
        viewed_posts = posts.filter(id__in=viewed_posts_id)
        return {'new_posts': new_posts, 'viewed_posts': viewed_posts}

    def show_users(self):
        untracked_users = User.objects.exclude(id__in=self.tracking_blogs.all()).exclude(id=self.owner_id)
        tracking_users = self.tracking_blogs.all()
        return {'untracked_users': untracked_users, 'tracking_users': tracking_users}


@transaction.atomic
@receiver(post_save, sender=User)
def create_user_page(sender, instance, created, **kwargs):
    if created:
        PersonalPage.objects.create(owner=instance, name=f'Блог пользователя: {instance.username}')


class PostItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=128)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(PersonalPage, on_delete=models.CASCADE, related_name='blog')

    def __str__(self):
        return f'{self.title}'


@receiver(post_save, sender=PostItem)
def send_notifications(sender, instance, created, **kwargs):
    if created:
        host = f'http://127.0.0.1:8000'
        msg = f'Появился новый пост: {instance.blog}. Прямая ссылка: {host}/post/{instance.id}'
        followed_blog = PersonalPage.objects.filter(tracking_blogs__personalpage=instance.blog)
        for owner in followed_blog.values('owner'):
            user = User.objects.get(id=owner['owner'])
            if user.email:
                print(msg)
                send_mail('Новый пост', msg, settings.EMAIL_HOST_USER, [user.email])


class ViewedPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostItem, on_delete=models.CASCADE)

    @staticmethod
    def mark_as_read(user, post):
        ViewedPosts.objects.create(user=user, post=post)

    @staticmethod
    def get_viewed_posts(user):
        return ViewedPosts.objects.filter(user=user).values('post_id')
