"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from django.conf.urls.static import static
from board import views as board_views #PostingViewSet, CommentViewSet, posting_comments
from mysite import settings


router = routers.DefaultRouter()
router.register(r'postings', board_views.PostingViewSet)
router.register(r'comments', board_views.CommentViewSet)

urlpatterns = [
    url(r'^api/postings/count/$', board_views.postings_pagecount),
    url(r'^api/postings/(?P<pk>\d+)/$', board_views.posting_with_pk),
    url(r'^api/postings/(?P<pk>\d+)/comments/$', board_views.posting_comments),
    url(r'^api/postings/$', board_views.posting_rest),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^board/$', board_views.BoardView.as_view()),
    url(r'^$', board_views.BoardView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
