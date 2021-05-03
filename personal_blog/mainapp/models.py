from uuid import uuid4

from django.db.models import UniqueConstraint
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
        return posts

    def show_users(self):
        untracked_users = User.objects.exclude(id__in=self.tracking_blogs.all()).exclude(id=self.owner_id)
        tracking_users = self.tracking_blogs.all()
        return {'untracked_users': untracked_users, 'tracking_users': tracking_users}

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

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

    def send_notifications(self):
        pass

    def __str__(self):
        return f'{self.title}'


class ViewedPosts(models.Model):
    class Meta:
        # unique_together = (('user', 'post'),)
        UniqueConstraint(fields=['user', 'post'], name='user_post_key')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostItem, on_delete=models.CASCADE)
