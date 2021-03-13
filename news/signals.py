from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string
from .models import Post, Author, Category, PostCategory, Comment, User, CategorySubscribers
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@receiver(m2m_changed, sender=Post.post_category.through)

def notify_subscribers_newscreation(sender, instance, **kwargs): #created,
    id = instance.id   # получаем ID побуликованной новости
    postCat = Post.objects.get(pk=id).post_category.all()  # получаем к каой категории она отностися
    for cat in postCat:   # пошли по категориям, к которым относится опубликованная новость
        #получаем емаил подписчиков. 
        emails_list = []  
        subscribers = User.objects.filter(category = cat)  #получили список подписчков.
        for subscriber_name in subscribers:  #итерируемся по списку - получаем имена
            subscriber_email = User.objects.get(username=str(subscriber_name)).email #из имен получаем емаил
            emails_list.append(subscriber_email)  #добавляем в список емаилов

        html_content = render_to_string( 
        'subscribe_created.html',
        {
        'title': instance.post_title, 'text':instance.article_text, 'art_id':id,
        }

        )

        msg = EmailMultiAlternatives(
        subject=f'Обновление в категории ',   
                
        body=f'Категоиря обновилась', 
        from_email='destpoch@yandex.ru',
        to=emails_list  
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send() # отсылаем

#m2m_changed.connect(notify_subscribers_newscreation, sender=Post.post_category.through)
