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

    def get_self_posts(self):
        pass

    def get_news_feed(self):
        posts = PostItem.objects.filter(blog__owner__in=self.tracking_blogs.values('id'))
        print(posts)
        return posts

    def __str__(self):
        return f'{self.name}'


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
