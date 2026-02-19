from rest_framework import viewsets
#from django_filters.rest_framework import DjangoFilterBackend
from .models import News
from .serializers import NewsSerializer
#from .filters import NewsFilter

# class NewsViewSet(viewsets.ModelViewSet):
#     queryset = News.objects.all()
#     serializer_class = NewsSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = NewsFilter



class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer

    # Define the internal keywords to filter news
    internal_keywords = ['Olymic','medal']

    def get_queryset(self):
        queryset = News.objects.all()
        for keyword in self.internal_keywords:
            queryset = queryset.filter(title__icontains=keyword)
        return queryset


