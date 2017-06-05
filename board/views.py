from django.shortcuts import render
from rest_framework import viewsets
from .models import Posting, Comment
from .serializers import (PostingSerializer, CommentSerializer, PostringDetailSerializer)
from .models import Posting, Comment
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import permissions
from django.forms.models import model_to_dict
from django.db import IntegrityError
from collections import OrderedDict
from .utils import dict_to_OreredDict
import mysite
# Create your views here.

class BoardView(TemplateView):
    template_name = 'board/board.html'

class PostingViewSet(viewsets.ModelViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@api_view(('GET', 'DELETE',)) # method not
@permission_classes((permissions.AllowAny,))
@csrf_exempt
@renderer_classes((JSONRenderer,))
def posting_with_pk(request, pk):
    #print('posting detail function !!')
    if (request.method == 'GET'):
        try:
            posting = Posting.objects.get(pk=pk)
        except Posting.DoesNotExist:
            return Response(None, status=404)
        serializer = PostringDetailSerializer(posting, context={'request' : request})
        return Response(serializer.data)

    if (request.method == 'DELETE'):
        try:
            Posting.objects.get(pk=pk).delete()
        except Posting.DoesNotExist:
            return Response(None, status=404)
        return Response(None, status=204)

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


@api_view(('GET', 'POST',))
@permission_classes((permissions.AllowAny,))
@csrf_exempt
@renderer_classes((JSONRenderer,))
def posting_rest(request):
    if (request.method == 'GET'):
        index = 0; pagesize = mysite.settings.REST_FRAMEWORK['PAGE_SIZE']; start = 0;
        if (request.GET.urlencode()):
            try:
                query_string = request.GET.urlencode().split('=')
                if (query_string[0] == 'page'):
                    index = int(query_string[1])
            except (IndexError , ValueError) as e:
                pass
            else:
                pagesize = mysite.settings.REST_FRAMEWORK['PAGE_SIZE']
                start = ((index - 1) * pagesize)

        postings = Posting.objects.all()[start:start + pagesize]
        if len(postings) == 0:
            return Response(None , 404)
        postinglist = []
        response_fields = ['id', 'title', 'name', 'create_date',]
        fields_ordering = ['id', 'title', 'name', 'create_date', 'comment_count', 'url']
        for posting in postings:
            postingdict = model_to_dict(posting, \
                fields=response_fields)
            postingdict['create_date'] = postingdict['create_date'].strftime('%Y-%m-%d %H:%M')
            comment_count = posting.comment_set.count()
            postingdict['comment_count'] = comment_count
            postingdict['url'] = '/api/postings/' + str(postingdict['id'])
            #ordering keyword for response
            orderedDict = dict_to_OreredDict(postingdict, fields_ordering)
            postinglist.append(orderedDict)
        return Response({'results' : postinglist})

    if (request.method == 'POST'):
        data= request.data
        try:
            Posting.objects.create(name=data['name'], title=data['title'], text=data['text'])
        except IntegrityError:
            Response(request.data, status=500)
        return Response(request.data)

@api_view(('GET',))
@permission_classes((permissions.AllowAny,))
@renderer_classes((JSONRenderer,))
def postings_pagecount(request):
    pageCount = Posting.objects.count()
    #print(pageCount)
    data = { 'count': pageCount, 'postingPerPage': mysite.settings.REST_FRAMEWORK['PAGE_SIZE']}
    return Response(data);
