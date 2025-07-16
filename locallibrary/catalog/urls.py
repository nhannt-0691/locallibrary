from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    # path('books/', views.book_list, name='book_list'),
    # path('authors/', views.author_list, name='author_list'),

]

