from django.shortcuts import render
from rest_framework import viewsets
from .models import Posting, Comment
from .serializers import (PostingSerializer, CommentSerializer, PostringDetailSerializer)
from .models import Posting, Comment
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

# Create your views here.

class BoardView(TemplateView):
    template_name = 'board/board.html'

class PostingViewSet(viewsets.ModelViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@csrf_exempt
def posting_detail(request, pk):
    print('posting detail function !!')
    try:
        posting = Posting.objects.get(pk=pk)
    except Posting.DoesNotExist:
        return HttpResponse(status=404)

    if (request.method == 'GET'):
        serializer = PostringDetailSerializer(posting, context={'request' : request})
        return JsonResponse(serializer.data)

@csrf_exempt
def posting_comments(request, pk):
    try:
        comments = Posting.objects.get(pk=pk).comment_set.all()
    except Posting.DoesNotExist:
        return HttpResponse(status=404)
    except Comment.DoesNotExist:
        return HttpResponse(status=404)
    if (len(comments) == 0):
        return HttpResponse(status=404)

    if (request.method == 'GET'):
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
