from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class Suggestion_Model(models.Model):
    suggestion = models.CharField(max_length=240)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        max_length=144,
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True)
    image_description = models.CharField(
        max_length=240,
        null=True,
        blank=True)

    def __str__(self):
        return self.author.username + " " + self.suggestion

class Comment_Model(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion_Model, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class NamedModel(models.Model):
    class Meta:
        abstract = True

    def getName(self):
        return self.__class__.__name__

class Subreddit(models.Model):
    title = models.CharField(max_length=30, blank=False, unique=True) #add validators here
    description = models.CharField(max_length=240, blank=True, default='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    #maybe retrieve thread count

    @property
    def subredditTitle(self):
        return self.title.replace(' ', '_')

    def get_absolute_url(self):
        return reverse('subredditPage', args=[self.subredditTitle])

    @staticmethod
    def getSubreddit(title):
        try:
            return Subreddit.objects.get(title=title)
        except ObjectDoesNotExist:
            return Subreddit.objects.get(title=title.replace('_',' '))

class Post(MPTTModel):
    title = models.CharField(max_length=50, unique=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    published_on = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    upvotes = models.IntegerField(blank=True, default=0)
    downvotes = models.IntegerField(blank=True, default=0)
    # uid = models.UUIDField(max_length=8, primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.title

    @property
    def score(self):
        return self.upvotes - self.downvotes

    class MPTTMeta:
        order_insertion_by = ['id']
