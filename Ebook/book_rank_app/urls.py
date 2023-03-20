# from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_list, name="list"),
    path('create', views.article_create, name="create"),
    # create/ 하면 이렇게만 써야됨.. 어떤게 맞는지 모르겠다.
    path('slug/<str:slug>', views.article_details, name="detail"),
]
