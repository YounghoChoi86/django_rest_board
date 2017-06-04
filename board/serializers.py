from django.conf.urls import url, include
from .models import Posting, Comment
from rest_framework import serializers

class PostingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posting
        fields = ('id', 'url', 'title', 'name', 'create_date')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('name', 'text')

class PostringDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posting
        fields = ('title', 'create_date', 'name', 'text')
