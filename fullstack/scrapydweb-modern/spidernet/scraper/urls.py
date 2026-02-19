from django.urls import path
from . import views

urlpatterns = [
    path('schedule/<str:spider_name>/', views.schedule_spider, name='schedule_spider'),
    path('jobs/', views.list_jobs, name='list_jobs'),
]
