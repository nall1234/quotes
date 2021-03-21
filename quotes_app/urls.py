from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('quotes', views.quotes),
    path('add_quote', views.add_quote),
    path('like_quote/<int:id>', views.like_quote),
    path('delete_quote/<int:id>', views.delete_quote),
    path('edit/<int:id>', views.edit),
    path('user/<int:id>', views.user),
]
