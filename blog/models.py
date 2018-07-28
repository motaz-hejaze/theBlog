from django.db import models
from django.urls import reverse

# Create your models here.
from django.utils import timezone

from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager , self).get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User , related_name='blog_posts', on_delete = models.CASCADE)
    # related_name for reverse relation from User to Post
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    # timezone is a zone time aware version of datetime 
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10 , choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='post_images')
    # the default manager
    objects = models.Manager()
    # our custom manager
    published = PublishedManager()
    # tagging system
    tags = TaggableManager()

    

    def get_absolute_url(self):
        return reverse('blog:post_detail' , args=[
            self.publish.year,
            self.publish.strftime('%m'),
            self.publish.strftime('%d'),
            self.slug,
        ])

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)

class Mailer(models.Model):
    host = models.CharField(max_length=50)
    user = models.EmailField()
    password = models.CharField(max_length=50)
    port = models.PositiveIntegerField()
    use_TLC = models.BooleanField(default=True)