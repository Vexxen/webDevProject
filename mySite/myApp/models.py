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
    # uid = models.UUIDField(max_length=8, primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['id']

# class Post(models.Model):
# class Post(MPTTModel, NamedModel):
#     uid = models.UUIDField(max_length=8, primary_key=True, default=uuid.uuid4, editable=False)
#     content = models.TextField(blank=True, default='')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     published_on = models.DateTimeField(auto_now_add=True, auto_now=False)
#     last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
#     parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
#     #ip_addr = models.GenericIPAddressField(blank=True, null=True)
#     #insert voting

#     def __init__(self, *args, **kwargs):
#         super(Post, self).__init__(*args, **kwargs)
#         #insert voting
    
#     class MPTTMetta:
#         order_insertion_by = ['created_on']

#     def __str_(self):
#         return self.content[:80]

#     @property
#     def thread(self):
#         post = self
#         while post.parent:
#             post = post.parent
#         return Thread.objects.get(op=post)

#     # @property
#     # def score(self):
#     #         return self.upvotes - self.downvotes

#     def getReplies(self, excluded=()):
#         replies = Post.objects.filter(parent=self.uid).exclude(excluded_uid=excluded)
#         for reply in replies:
#             replies |= reply.getReplies(excluded=excluded)
#         return replies

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# class Thread(models.Model):
#     title = models.CharField(max_length=80, blank=False)
#     # slug = models.SlugField(unique=False, null=True)
#     body = models.TextField()
#     url = models.URLField(max_length=120, blank=True, default='')
#     # views = models.IntegerField(blank=True, default=0)
#     subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
#     # op = models.ForeignKey('Post', related_name='+', on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         self.slug = self._genSlug()
#         super(Thread, self).save(*args, **kwargs)

#     def delete(self, *args, **kwargs):
#         try:
#             self.op.delete()
#         except Post.DoesNotExist:
#             pass
#         super(Thread, self).delete(*args, **kwargs)

#     def _genSlug(self):
#         slug = slugify(self.title, to_lower=True, max_length=80)
#         return slug
    
#     @property
#     def relativeUrl(self):
#         return reverse('threadPage', args=[self.subreddit.urlTitle, self.id, self.slug])

#     def get_absolute_url(self):
#             return self.relativeUrl