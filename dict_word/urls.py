from django.urls import path
from . import views

app_name = 'dict_word'

urlpatterns = [
    path('', views.dict_word_index, name='dict_index'),
    path('spider/', views.dict_word_spider, name='dict_word_spider'),
]