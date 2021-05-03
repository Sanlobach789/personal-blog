from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='index'),
    path('news_feed/', mainapp.news_feed, name='news_feed'),
    path('post/<uuid:post_id>/', mainapp.post_content, name='post'),
    path('blogs/', mainapp.users_list, name='blogs'),
    path('subscribe/<uuid:user_id>/', mainapp.subscribe, name='subscribe'),
    path('unsubscribe/<uuid:user_id>/', mainapp.unsubscribe, name='unsubscribe'),
    path('new-post/', mainapp.create_new_post, name='new_post'),
    path('del-post/<uuid:post_id>/', mainapp.delete_post, name='delete_post'),
    path('mark-post/<uuid:post_id>/', mainapp.mark_post_as_read, name='mark_post'),
]
