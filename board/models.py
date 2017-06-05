from django.db import models
from datetime import datetime

# Create your models here.

class PostingManager(models.Manager):
    def create(self, **kwargs):
        kwargs['create_date'] = datetime.now()
        kwargs['modified_date'] = datetime.now()
        item = super(PostingManager, self).create(**kwargs)
        return item

class Posting(models.Model):
    name = models.CharField(max_length=30, blank=False)
    title = models.CharField(max_length=100, blank=False)
    text = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    objects = PostingManager()
    class Meta:
        ordering = ['-create_date']
    def __str__(self):
        return self.name + ':' + self.title

class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False)
    text = models.CharField(max_length=200, blank=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        ordering = ['-create_date']
        return self.name + ':' + self.text
