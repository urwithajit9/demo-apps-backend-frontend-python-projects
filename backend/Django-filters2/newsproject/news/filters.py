import django_filters
from .models import News

class NewsFilter(django_filters.FilterSet):
    keywords = django_filters.CharFilter(method='filter_by_keywords')

    class Meta:
        model = News
        fields = ['keywords']

    def filter_by_keywords(self, queryset, name, value):
        #keywords = value.split(',')
        keywords = ['Olymic','medal']
        for keyword in keywords:
            queryset = queryset.filter(title__icontains=keyword.strip())
        return queryset
