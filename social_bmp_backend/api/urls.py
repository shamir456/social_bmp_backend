from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

from social_bmp_backend.api import views



urlpatterns = [
    path('posts/', views.PostsViewSet.as_view(),name='posts-api'),
    url(r'^add/', views.PostsCreateSet.as_view(), name='post-list'),
    path('post/<int:id>/', views.PostListView.as_view()),
    path('comments/authors/',views.AuthorViewSet.as_view(),name='author-list'),
    path('comments/sentiment/',views.SentimentViewSet.as_view(),name='sentiment-list'),
    path('posts/count/',views.DataViewSet.as_view(),name='post-count'),
    path('comments/lang',views.LanguageViewSet.as_view(),name='lang-count')

]

urlpatterns = format_suffix_patterns(urlpatterns)
