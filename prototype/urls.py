from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scraping/', views.scraping, name='scraping'),
    path('analysis', views.analysis, name='analysis'),
]
