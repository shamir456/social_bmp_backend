from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from social_bmp_backend.api import views

urlpatterns = [
    path('posts/', views.PostsViewSet.as_view(),name='posts-api'),
    #path('snippets/<int:pk>/', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
